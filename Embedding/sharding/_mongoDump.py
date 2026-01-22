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


config = {
    # Source (sharded cluster mongos)
    "sourceUri": os.getenv("MONGO_CONNECTION_STRING"),
    "sourceDb": "eCommerceProjectEmbedding",
    "sourceCollection": "orders",

    # Dump folder
    "outDir": "./Embedding/sharding/dumpOrders",

    # Safety: dry-run unless confirm True
    "confirm": False,
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
