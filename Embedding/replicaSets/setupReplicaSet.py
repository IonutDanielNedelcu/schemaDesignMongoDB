import subprocess
import time
import sys
from pymongo import MongoClient
from pymongo.errors import OperationFailure, ConnectionFailure

# Configuration
networkName = "mongo-ecommerce-net"
replicaSetName = "rs0"
nodes = [
    {"name": "mongo1", "port": 27017},
    {"name": "mongo2", "port": 27018},
    {"name": "mongo3", "port": 27019}
]

def runCommand(command):
    try:
        subprocess.run(command, check=True, shell=True, stdout=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        print(f"    Error executing: {command}")
        return False

def setupInfrastructure():
    print("Starting Infrastructure")
    
    # 1. Cleanup old containers
    print("Cleaning up old containers...")
    containerNames = " ".join([n["name"] for n in nodes])
    runCommand(f"docker rm -f {containerNames}")
    runCommand(f"docker network rm {networkName}")

    # 2. Create network
    print(f"Creating network: {networkName}")
    runCommand(f"docker network create {networkName}")

    # 3. Start nodes
    for node in nodes:
        print(f"    Starting container: {node['name']} on port {node['port']}...")
        cmd = (
            f"docker run -d --name {node['name']} "
            f"-p {node['port']}:27017 "
            f"--net {networkName} "
            f"mongo:6.0 "
            f"--replSet {replicaSetName} "
            f"--bind_ip_all"
        )
        runCommand(cmd)
    
    print("Waiting 15 seconds for MongoDB processes to boot...")
    time.sleep(15)

def initReplicaSet():
    print("\n    Initializing Replica Set")
    
    try:
        client = MongoClient("localhost", 27017, directConnection=True)
    except Exception as e:
        print(f"    Connection error: {e}")
        sys.exit(1)

    rsConfig = {
        "_id": replicaSetName,
        "members": [
            {"_id": 0, "host": "mongo1:27017"},
            {"_id": 1, "host": "mongo2:27017"},
            {"_id": 2, "host": "mongo3:27017"}
        ]
    }

    try:
        print("    Sending replSetInitiate command...")
        client.admin.command("replSetInitiate", rsConfig)
        print("    Replica Set configuration sent.")
    except OperationFailure as e:
        if "already initialized" in str(e):
            print("    Replica Set already initialized.")
        else:
            print(f"    MongoDB Error: {e}")
    finally:
        client.close()

def verifyPrimary():
    print("\n    Verifying Primary Election ---")
    print("    Checking cluster status (polling every 2s)...")

    # We reconnect. This time we can use directConnection=True to ask node1 specifically
    # "Who is the primary?"
    client = MongoClient("localhost", 27017, directConnection=True)
    
    maxRetries = 15 # Wait up to 30 seconds (15 * 2s)
    
    for attempt in range(maxRetries):
        try:
            # The 'hello' command returns the server status including who is primary
            # (It replaces the old 'isMaster' command)
            status = client.admin.command("hello")
            
            primaryHost = status.get("primary")
            setName = status.get("setName")
            isPrimary = status.get("isWritablePrimary") # boolean

            if primaryHost:
                print(f"    Primary FOUND: {primaryHost}")
                print(f"    Replica Set Name: {setName}")
                
                if isPrimary:
                    print("  (Connected directly to the Primary node)")
                else:
                    print("  (Connected to a Secondary, but it knows who the Primary is)")
                return
            else:
                print(f"    Attempt {attempt + 1}/{maxRetries}: Election in progress... waiting...")
        
        except (ConnectionFailure, OperationFailure) as e:
             print(f"    Attempt {attempt + 1}/{maxRetries}: Connection glitch ({e}). Retrying...")

        time.sleep(2)
    
    print("    ERROR: Timed out waiting for a Primary to be elected.")
    client.close()

if __name__ == "__main__":
    setupInfrastructure()
    initReplicaSet()
    verifyPrimary()
    print("\n    Done. Cluster is ready.")