# Sharding tools

Files:

- `apply_sharding.py` — safe script to apply sharding to a collection. By default it runs in dry-run mode; add `--confirm` to execute.

Usage (programmatic):

Edit the `config` dictionary at the bottom of `apply_sharding.py` or import `runApplySharding` from the module and call it directly from Python.

Example (editing `apply_sharding.py` defaults):

```bash
# Open the file and set `confirm` to True once you're ready to apply.
python apply_sharding.py
```

Example (importing from another script):

```python
from apply_sharding import runApplySharding

runApplySharding(
	mongoUri="mongodb://user:pass@mongos-host:27017",
	dbName="eCommerceProjectEmbedding",
	collectionName="orders",
	shardKey="user_id",
	strategy="hashed",
	confirm=True,
)
```

Notes and safety:
- The script expects to run against a `mongos` process. It will warn if connected directly to a replica set member.
- The script calls `enableSharding` and `shardCollection` admin commands.
- It reports chunk counts per shard from the `config.chunks` collection (an estimate of distribution). It does not move chunks for balancing; for large clusters rely on the balancer.
- Always test first in a staging environment and ensure you have backups.

Dump & restore (recommended way to remove sharding):

I added `mongoDump.py` which performs a safe `mongodump` from the sharded cluster and writes the dump to `outDir`.

Quick steps:

- Edit `mongoDump.py` `config` dictionary: set `sourceUri` (or `MONGO_CONNECTION_STRING` env), `sourceDb`, `sourceCollection`, and `outDir`.
- By default the script runs a dry-run and prints the exact `mongodump` command. Set `confirm=True` in the config to execute.

Example (dry-run):

```bash
python mongoDump.py
```

Example (execute):

```bash
# edit mongoDump.py and set config['confirm'] = True, then:
python mongoDump.py
```

Notes:
- Ensure `mongodump` and `mongorestore` (MongoDB Database Tools) are on PATH.
- The script restores into `targetDb` on `targetUri`. If you want to restore into the same cluster as unsharded,
  restore to a standalone instance or remove sharding metadata first (advanced & risky).
- The script supports `dropOnRestore` to overwrite the target collection.
