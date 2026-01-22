import os
import subprocess
import time
import socket
from dotenv import load_dotenv

load_dotenv()


def runCommand(cmd, check=True):
    print("Running:", " ".join(cmd))
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(proc.stdout)
    if check and proc.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nExit: {proc.returncode}")
    return proc


def waitForTcp(host, port, timeout=30):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection((host, port), timeout=2):
                return True
        except Exception:
            time.sleep(1)
    return False


def cleanupOldContainers():
    names = [config["configSvr"]["name"]] + [s["name"] for s in config["shards"]] + [config["mongos"]["name"]]
    for name in names:
        print(f"Removing existing container if present: {name}")
        runCommand(["docker", "rm", "-f", name], check=False)

    print(f"Removing network if present: {config['network']}")
    runCommand(["docker", "network", "rm", config["network"]], check=False)


config = {
    "network": "mongo-shard-net",
    "image": os.getenv("MONGO_DOCKER_IMAGE", "mongo:6"),
    "configSvr": {"name": "cs1", "port": 27019, "replSet": "configReplSet"},
    "shards": [
        {"name": "shard1", "port": 27018, "replSet": "rs1"},
        {"name": "shard2", "port": 27020, "replSet": "rs2"},
        {"name": "shard3", "port": 27021, "replSet": "rs3"},
    ],
    "mongos": {"name": "mongos", "port": 27017},
    
    # confirm=False => dry-run only; set True to execute
    "confirm": False,
}


def createNetwork():
    runCommand(["docker", "network", "create", config["network"]], check=False)


def startConfigServer():
    cs = config["configSvr"]
    cmd = [
        "docker", "run", "-d",
        "--name", cs["name"],
        "--net", config["network"],
        "-p", f"{cs['port']}:{cs['port']}",
        config["image"],
        "mongod",
        "--configsvr",
        "--replSet", cs["replSet"],
        "--bind_ip_all",
        "--port", str(cs["port"]),
    ]
    runCommand(cmd, check=config["confirm"])
    if config["confirm"]:
        print(f"Waiting for config server {cs['name']} on port {cs['port']}...")
        if waitForTcp("localhost", cs["port"], timeout=30):
            print("Config server reachable")
        else:
            print("Warning: config server port not reachable after timeout")


def startShards():
    for s in config["shards"]:
        cmd = [
            "docker", "run", "-d",
            "--name", s["name"],
            "--net", config["network"],
            "-p", f"{s['port']}:{s['port']}",
            config["image"],
            "mongod",
            "--shardsvr",
            "--replSet", s["replSet"],
            "--bind_ip_all",
            "--port", str(s["port"]),
        ]
        runCommand(cmd, check=config["confirm"])
        if config["confirm"]:
            print(f"Waiting for shard {s['name']} on port {s['port']}...")
            if waitForTcp("localhost", s["port"], timeout=30):
                print(f"Shard {s['name']} reachable")
            else:
                print(f"Warning: shard {s['name']} port not reachable after timeout")


def startMongos():
    cs = config["configSvr"]
    cfgString = f"{cs['replSet']}/{cs['name']}:{cs['port']}"
    m = config["mongos"]
    cmd = [
        "docker", "run", "-d",
        "--name", m["name"],
        "--net", config["network"],
        "-p", f"{m['port']}:{m['port']}",
        config["image"],
        "mongos",
        "--configdb", cfgString,
        "--bind_ip_all",
        "--port", str(m["port"]),
    ]
    runCommand(cmd, check=config["confirm"])
    if config["confirm"]:
        m = config["mongos"]
        print(f"Waiting for mongos on port {m['port']}...")
        if waitForTcp("localhost", m["port"], timeout=30):
            print("Mongos reachable")
        else:
            print("Warning: mongos port not reachable after timeout")


def initiateReplica(container, replSetName, port):
    js = (
        "rs.initiate({ _id: \"%s\", members: [ { _id: 0, host: \"%s:%s\" } ] })"
        % (replSetName, container, port)
    )
    cmd = ["docker", "exec", container, "mongosh", "--port", str(port), "--eval", js]
    runCommand(cmd, check=config["confirm"])


def addShardsToMongos():
    try:
        from connection import connectToMongoDB, closeConnection
    except Exception as e:
        print("Could not import connection helper (pymongo may be missing):", e)
        return

    client, db = connectToMongoDB()  # uses MONGO_CONNECTION_STRING_SHARDING env var
    if not client:
        print("Connection to mongos failed")
        return

    try:
        try:
            client.admin.command("ping")
        except Exception as e:
            print("Could not reach mongos:", e)
            return

        for s in config["shards"]:
            shardStr = f"{s['replSet']}/{s['name']}:{s['port']}"
            print("Adding shard:", shardStr)
            try:
                client.admin.command("addShard", shardStr)
            except Exception as e:
                print(f"addShard failed for {shardStr}: {e}")
    finally:
        closeConnection(client)


def main():
    print("Configuration:")
    print(config)

    if not config["confirm"]:
        print("Dry-run mode. To actually create containers and configure the cluster, set config['confirm']=True in this script or pass via env var MONGO_SHARD_CONFIRM=1")

    if config["confirm"]:
        # cleanup any previous containers/networks with the same names
        cleanupOldContainers()

        createNetwork()
        startConfigServer()
        time.sleep(3)

        startShards()
        time.sleep(5)

        cs = config["configSvr"]
        print("Initiating config server replica set.")
        initiateReplica(cs["name"], cs["replSet"], cs["port"])
        time.sleep(3)

        for s in config["shards"]:
            print(f"Initiating replset {s['replSet']} on {s['name']}:{s['port']}")
            initiateReplica(s["name"], s["replSet"], s["port"])
            time.sleep(2)

        startMongos()
        time.sleep(3)

        addShardsToMongos()

        print("Cluster setup attempted. Check container logs for details.")


if __name__ == "__main__":
    if os.getenv("MONGO_SHARD_CONFIRM") in ("1", "true", "True"):
        config["confirm"] = True
    main()
