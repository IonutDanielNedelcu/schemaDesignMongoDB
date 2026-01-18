"""
Simple mongodump helper script.

This script only performs `mongodump` from a source (typically a mongos) and
writes the dump to `outDir`. By default it performs a dry-run and prints the
command; set `confirm=True` in `config` to actually run.

Ensure `mongodump` (MongoDB Database Tools) is installed and on PATH.
"""
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def runCommand(cmd):
    print("Running:", " ".join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        print(line.rstrip())
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed with code {proc.returncode}")


def mongodump(mongoUri, dbName, collectionName, outDir, confirm=False):
    outPath = Path(outDir).resolve()
    cmd = [
        "mongodump",
        f"--uri={mongoUri}",
        "--db",
        dbName,
        "--collection",
        collectionName,
        "--out",
        str(outPath),
    ]

    if not confirm:
        print("Dry-run mongodump:")
        print(" ", " ".join(cmd))
        return str(outPath / dbName / f"{collectionName}.bson")

    runCommand(cmd)
    return str(outPath / dbName / f"{collectionName}.bson")


# Default config: edit as needed
config = {
    # Source (sharded cluster mongos)
    "sourceUri": os.getenv("MONGO_CONNECTION_STRING"),
    "sourceDb": "eCommerceProjectHybrid",
    "sourceCollection": "vendors",

    # Dump folder
    "outDir": "./Hybrid/sharding/dumpVendors",

    # Safety: dry-run unless confirm True
    "confirm": True,
}


def main():
    srcUri = config["sourceUri"]
    if not srcUri:
        print("Set MONGO_CONNECTION_STRING environment variable or edit config['sourceUri']")
        return

    dumpPath = mongodump(srcUri, config["sourceDb"], config["sourceCollection"], config["outDir"], confirm=config["confirm"])

    if not config["confirm"]:
        print("Dry-run complete. To actually run mongodump, set config['confirm']=True and re-run.")
        return

    print(f"Dump completed: {dumpPath}")


if __name__ == "__main__":
    main()
