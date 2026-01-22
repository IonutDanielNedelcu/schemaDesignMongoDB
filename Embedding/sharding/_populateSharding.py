import os
import json
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()


config = {
	"mongoUri": os.getenv("MONGO_CONNECTION_STRING_SHARDING"),
	"dbName": "eCommerceProjectEmbedding",
	"collections": [
		{"name": "orders", "folder": "JsonOrders", "shardKey": "user_id", "strategy": "hashed"},
		{"name": "products", "folder": "JsonProducts", "shardKey": "sku", "strategy": "hashed"},
		{"name": "users", "folder": "JsonUsers", "shardKey": "_id", "strategy": "hashed"},
	],
 
	# Safety: dry-run unless confirm True
	"confirm": True,
 
	# batch size for inserts - change depending on user CPU capacity
	"batchSize": 500,
}


def getClient(mongoUri=None):
	mongoUri = mongoUri or config["mongoUri"]
	return MongoClient(mongoUri, serverSelectionTimeoutMS=5000)


def enableShardingForDb(client, dbName):
	admin = client.admin
	print(f"Enabling sharding for database '{dbName}'")
	try:
		admin.command("enableSharding", dbName)
		print("enableSharding OK")
	except PyMongoError as e:
		print(f"enableSharding failed or already enabled: {e}")


def shardCollection(client, dbName, collName, shardKey, strategy="hashed"):
	admin = client.admin
	ns = f"{dbName}.{collName}"
	key = {shardKey: "hashed"} if strategy == "hashed" else {shardKey: 1}
	print(f"Sharding collection {ns} with key {key}")
	try:
		admin.command("shardCollection", ns, key=key)
		print("shardCollection OK")
	except PyMongoError as e:
		print(f"shardCollection failed: {e}")


def importJsonFolder(client, dbName, collName, folderPath, batchSize=1000):
	folder = Path(folderPath)
	if not folder.exists():
		print(f"Folder not found: {folder}")
		return

	coll = client[dbName][collName]
	files = sorted([p for p in folder.iterdir() if p.suffix.lower() == ".json"])
	if not files:
		print(f"No .json files found in {folder}")
		return

	for f in files:
		print(f"Importing {f} into {dbName}.{collName} ...")
		try:
			text = f.read_text(encoding="utf-8")
			data = json.loads(text)
			# If data is a list, insert_many; if dict, insert_one
			if isinstance(data, list):
				for i in range(0, len(data), batchSize):
					batch = data[i : i + batchSize]
					coll.insert_many(batch)
			elif isinstance(data, dict):
				coll.insert_one(data)
			else:
				print(f"Unsupported JSON root type in {f}")

		except json.JSONDecodeError:
			# fallback: try JSON Lines
			with f.open(encoding="utf-8") as fh:
				batch = []
				for line in fh:
					line = line.strip()
					if not line:
						continue
					try:
						obj = json.loads(line)
					except json.JSONDecodeError:
						print(f"Skipping invalid JSON line in {f}")
						continue
					batch.append(obj)
					if len(batch) >= batchSize:
						coll.insert_many(batch)
						batch = []
				if batch:
					coll.insert_many(batch)
		except Exception as e:
			print(f"Failed to import {f}: {e}")


def runPopulateSharding():
	print("Configuration:")
	print(config)

	# resolve folder paths relative to this file
	base = Path(__file__).parent
	for c in config["collections"]:
		c["folderPath"] = base / c["folder"]

	if not config["confirm"]:
		return

	client = None
	try:
		client = getClient()
		client.admin.command("ping")
	except Exception as e:
		print(f"Could not connect to mongos: {e}")
		return

	try:
		enableShardingForDb(client, config["dbName"])
		for c in config["collections"]:
			shardCollection(client, config["dbName"], c["name"], c["shardKey"], c.get("strategy", "hashed"))
			importJsonFolder(client, config["dbName"], c["name"], c["folderPath"], batchSize=config["batchSize"])

	finally:
		if client:
			client.close()


if __name__ == "__main__":
	# allow enabling confirm via env var for convenience
	if os.getenv("POPULATE_SHARDING_CONFIRM") in ("1", "true", "True"):
		config["confirm"] = True
	runPopulateSharding()

