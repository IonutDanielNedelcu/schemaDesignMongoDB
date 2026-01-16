
import os
import json
import time
import subprocess
import argparse
import importlib.util
from pathlib import Path
from datetime import datetime, timezone
from pymongo import MongoClient, errors


def loadMapping():
    """Load node list from setupReplicaSet.py and return mapping {replicaSetName: [members]}.

    Each member is a dict with at least 'name' and 'hostPort' keys to match older callers.
    """
    base = Path(__file__).parent
    setup_path = base / "setupReplicaSet.py"
    if not setup_path.exists():
        raise FileNotFoundError(f"setupReplicaSet.py not found at {setup_path}")

    spec = importlib.util.spec_from_file_location("setupReplicaSet", str(setup_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    nodes = getattr(mod, 'nodes', None)
    rset = getattr(mod, 'replicaSetName', getattr(mod, 'REPLICA_SET_NAME', None))
    if not nodes or not isinstance(nodes, list) or not rset:
        raise RuntimeError("setupReplicaSet.py must define 'nodes' (list) and 'replicaSetName' or 'REPLICA_SET_NAME'")

    members = []
    for n in nodes:
        if isinstance(n, dict) and 'name' in n and 'port' in n:
            members.append({'name': n['name'], 'hostPort': n['port']})

    return {rset: members}


def containerForPort(mapping, repl, port):
    for m in mapping.get(repl, []):
        try:
            if int(m.get("hostPort")) == int(port):
                return m.get("name")
        except Exception:
            continue
    return None


def runCmd(cmd):
    print("Running:", " ".join(cmd))
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repl", default=None, help="Replica set to test (uses setupReplicaSet.py default if omitted)")
    parser.add_argument("--db", default="test", help="Database name to use for testing")
    parser.add_argument("--output", default="replicaFailover_log.ndjson", help="NDJSON output file to append events to")
    args = parser.parse_args()

    outputFile = os.path.abspath(args.output)

    def logEvent(evt: dict):
        # use timezone-aware UTC timestamps
        evt.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
        try:
            outdir = os.path.dirname(outputFile)
            if outdir and not os.path.exists(outdir):
                os.makedirs(outdir, exist_ok=True)
            with open(outputFile, "a", encoding="utf-8") as of:
                of.write(json.dumps(evt, default=str) + "\n")
        except Exception as e:
            print("Failed to write log event:", e)
        print("LOG:", evt.get("type", "event"), evt.get("msg", ""))

    mapping = loadMapping()
    # if repl not provided, pick the only available one
    if not args.repl:
        args.repl = next(iter(mapping.keys()))

    if args.repl not in mapping:
        print(f"Replica set {args.repl} not found in setupReplicaSet.py")
        return

    members = mapping[args.repl]
    seeds = [f"localhost:{m['hostPort']}" for m in members]
    mongoUri = f"mongodb://{','.join(seeds)}/?replicaSet={args.repl}"

    print("Connecting to replica set using URI:", mongoUri)
    logEvent({"type": "start_test", "repl": args.repl, "seeds": seeds, "mongoUri": mongoUri, "outputFile": outputFile})
    try:
        client = MongoClient(mongoUri, serverSelectionTimeoutMS=5000)
    except Exception as e:
        print("MongoClient init failed:", e)
        logEvent({"type": "connect_failed", "error": str(e)})
        return

    # perform initial write to ensure connectivity; wait for a primary first
    coll = client[args.db].failover_test
    wait_start = time.time()
    wait_timeout = 30
    while time.time() - wait_start < wait_timeout:
        try:
            if client.primary:
                break
        except Exception:
            pass
        time.sleep(1)

    if not client.primary:
        msg = f"No replica set primary detected within {wait_timeout}s"
        print(msg)
        logEvent({"type": "initial_write", "success": False, "error": msg})
        return

    try:
        res = coll.insert_one({"step": "initial", "time": time.time()})
        print("Initial write succeeded, _id:", res.inserted_id)
        logEvent({"type": "initial_write", "success": True, "inserted_id": str(res.inserted_id)})
    except Exception as e:
        print("Initial write failed:", e)
        logEvent({"type": "initial_write", "success": False, "error": str(e)})
        return

    primary = client.primary
    print("Current primary (host,port):", primary)
    if not primary:
        print("Could not determine primary from client. Aborting.")
        logEvent({"type": "no_primary_detected"})
        return
    primary_port = primary[1]
    primary_container = containerForPort(mapping, args.repl, primary_port)
    if not primary_container:
        print("Could not map primary port to a container. Aborting failover test.")
        return

    print(f"Stopping primary container {primary_container} to force failover...")
    stop = runCmd(["docker", "stop", primary_container])
    logEvent({"type": "stop_primary", "container": primary_container, "returncode": stop.returncode, "output": stop.stdout})
    if stop.returncode != 0:
        print("Failed to stop container:\n", stop.stdout)
        logEvent({"type": "stop_primary_failed", "container": primary_container, "output": stop.stdout})
        return

    # wait for election and retry writes
    start = time.time()
    timeout = 60
    success = False
    attempt = 0
    while time.time() - start < timeout:
        attempt += 1
        try:
            res = coll.insert_one({"step": "after-fail", "time": time.time(), "attempt": attempt})
            print("Write after failover succeeded, _id:", res.inserted_id)
            logEvent({"type": "write_after_fail", "success": True, "inserted_id": str(res.inserted_id), "attempt": attempt, "elapsed_s": time.time()-start})
            success = True
            break
        except errors.AutoReconnect as e:
            print("AutoReconnect, waiting for new primary...", str(e))
            logEvent({"type": "write_attempt", "success": False, "error": "AutoReconnect", "msg": str(e), "attempt": attempt})
        except Exception as e:
            print("Write failed (will retry):", str(e))
            logEvent({"type": "write_attempt", "success": False, "error": str(e), "attempt": attempt})
        time.sleep(2)

    if not success:
        print("Failover write did not succeed within timeout")
        logEvent({"type": "failover_result", "success": False, "elapsed_s": time.time()-start})
    else:
        try:
            docs = list(coll.find({}, limit=5))
            print(f"Read {len(docs)} docs from collection after failover (sample):")
            for d in docs:
                print(d)
            logEvent({"type": "read_after_fail", "count": len(docs), "sample_ids": [str(d.get("_id")) for d in docs]})
        except Exception as e:
            print("Read failed after failover:", e)
            logEvent({"type": "read_after_fail", "error": str(e)})

    # restart stopped container
    print(f"Starting container {primary_container} back up...")
    start_proc = runCmd(["docker", "start", primary_container])
    logEvent({"type": "start_primary", "container": primary_container, "returncode": start_proc.returncode, "output": start_proc.stdout})
    if start_proc.returncode == 0:
        print("Container started.")
    else:
        print("Failed to start container:\n", start_proc.stdout)
        logEvent({"type": "start_primary_failed", "container": primary_container, "output": start_proc.stdout})

    logEvent({"type": "test_finished", "success": success})


if __name__ == "__main__":
    main()
