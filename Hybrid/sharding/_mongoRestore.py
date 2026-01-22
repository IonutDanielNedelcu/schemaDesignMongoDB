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


def mongorestore(mongoUri, dbName, collectionName, bsonPath, confirm=False):
    bsonPath = Path(bsonPath).resolve()
    cmd = [
        "mongorestore",
        f"--uri={mongoUri}",
        "--db",
        dbName,
        "--collection",
        collectionName,
        "--drop",
        str(bsonPath),
    ]

    if not confirm:
        print("Dry-run mongorestore:")
        print(" ", " ".join(cmd))
        return str(bsonPath)

    if not bsonPath.exists():
        raise FileNotFoundError(f"BSON file not found: {bsonPath}")

    runCommand(cmd)
    return str(bsonPath)



config = {
    # Target (where to restore)
    "targetUri": os.getenv("MONGO_CONNECTION_STRING"),
    "targetDb": "eCommerceProjectEmbedding",
    "targetCollection": "orders",

    # Path to .bson file produced by mongodump
    "bsonPath": "./Embedding/sharding/dumpOrders/orders.bson",

    # Safety: dry-run unless confirm True
    "confirm": False,
}


def main():
    tgtUri = config["targetUri"]
    if not tgtUri:
        print("Set MONGO_CONNECTION_STRING environment variable or edit config['targetUri']")
        return

    bsonPath = Path(config["bsonPath"]).resolve()

    try:
        restored = mongorestore(tgtUri, config["targetDb"], config["targetCollection"], bsonPath, confirm=config["confirm"])
    except Exception as e:
        print("Restore failed:", e)
        return

    if not config["confirm"]:
        print("Dry-run complete. To actually run mongorestore, set config['confirm']=True and re-run.")
        return

    print(f"Restore completed from: {restored}")


if __name__ == "__main__":
    main()
