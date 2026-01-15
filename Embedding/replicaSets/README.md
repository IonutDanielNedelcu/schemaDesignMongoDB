# Replica Sets (local Docker)

This folder contains scripts to create and test a single MongoDB replica set
running in local Docker containers. Important: this is NOT a sharded cluster —
no config servers or `mongos` are created.

Files
- `setupReplicaSets.py`: creates a single replica set (`rs1`) with three
  members (`node_1`, `node_2`, `node_3`). Dry-run by default; set
  `MONGO_REPL_CONFIRM=1` to actually create containers and initiate the
  replica set.
- `containers.json`: mapping of replica set member container names to host
  ports (written by `setupReplicaSets.py` when executed).
- `testFailover.py`: simple read/write failover test which stops the primary
  container for a replica set to verify re-election and continued availability.

Quick start

1) Dry-run to print commands:

```bash
python Embedding/replicaSets/setupReplicaSets.py
```

2) Execute and create containers (PowerShell):

```powershell
$env:MONGO_REPL_CONFIRM = "1"
python Embedding/replicaSets/setupReplicaSets.py
```

3) Run failover test (after containers are up and replica sets initiated):

```bash
python Embedding/replicaSets/testFailover.py --repl rs1
```

Notes
- Docker must be running and available on PATH.
- `pymongo` is required for `testFailover.py` (`pip install pymongo`).
- Ports used by default: 27111–27113 for the three replica set members.

If you want a `docker-compose.yml` instead of `docker run` commands, I can
add one that starts all containers and networks together.
