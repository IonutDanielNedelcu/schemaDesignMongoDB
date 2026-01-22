import os
import json
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import subprocess
import shutil

load_dotenv()


config = {
	"mongoUri": os.getenv("MONGO_CONNECTION_STRING_SHARDING"),
	"dbName": "eCommerceProjectHybrid",
	"collections": [
		{"name": "orders", "folder": "dumpOrders", "shardKey": "user.userIdSnapshot", "strategy": "hashed"},
		{"name": "products", "folder": "dumpProducts", "shardKey": "sku", "strategy": "hashed"},
		{"name": "users", "folder": "dumpUsers", "shardKey": "_id", "strategy": "hashed"},
		{"name": "vendors", "folder": "dumpVendors", "shardKey": "_id", "strategy": "hashed"},
		{"name": "categories", "folder": "dumpCategories", "shardKey": "_id", "strategy": "hashed"},
	],
 
	# Safety: dry-run by default; set env POPULATE_SHARDING_CONFIRM=1 to enable
	"confirm": True,
 
	# batch size for inserts
	"batchSize": 500,
}


def getClient(mongoUri=None):
	mongoUri = mongoUri or config["mongoUri"]
	return MongoClient(mongoUri, serverSelectionTimeoutMS=5000)


def enableShardingForDb(client, dbName):
	admin = client.admin
	print(f"Enabling sharding for database '{dbName}'...")
	try:
		admin.command("enableSharding", dbName)
		print("enableSharding OK")
	except PyMongoError as e:
		print(f"enableSharding failed or already enabled: {e}")


def shardCollection(client, dbName, collName, shardKey, strategy="hashed"):
	admin = client.admin
	ns = f"{dbName}.{collName}"
	key = {shardKey: "hashed"} if strategy == "hashed" else {shardKey: 1}
	print(f"Sharding collection {ns} with key {key}...")
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
 
	bsonFiles = list(folder.rglob('*.bson'))
	if bsonFiles:
		mongorestorePath = shutil.which('mongorestore')
		if not mongorestorePath:
			print("mongorestore not found in PATH; cannot restore BSON dumps. Skipping BSON restore.")
		else:
			for bsonFile in sorted(bsonFiles):
    
				collFileName = bsonFile.name
				collNameFromFile = collFileName.rsplit('.', 1)[0]
				print(f"Restoring BSON {bsonFile} into {dbName}.{collName} (file collection: {collNameFromFile}) ...")
    
				targetCollection = collName if collNameFromFile == collName else collNameFromFile
				cmd = [mongorestorePath, '--uri', config.get('mongoUri') or '', '--db', dbName, '--collection', targetCollection, '--noIndexRestore', str(bsonFile)]
				try:
					subprocess.run(cmd, check=True)
					print(f"mongorestore completed for {bsonFile}")
				except subprocess.CalledProcessError as e:
					print(f"mongorestore failed for {bsonFile}: {e}")
		return

	# Fallback: import JSON files (existing behaviour)
	coll = client[dbName][collName]
	files = sorted([p for p in folder.iterdir() if p.suffix.lower() == ".json"])
	if not files:
		print(f"No .json files found in {folder}")
		return

	for jsonFile in files:
		print(f"Importing {jsonFile} into {dbName}.{collName} ...")
		try:
			text = jsonFile.read_text(encoding="utf-8")
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
			with jsonFile.open(encoding="utf-8") as fh:
				batch = []
				for line in fh:
					line = line.strip()
					if not line:
						continue
					try:
						obj = json.loads(line)
					except json.JSONDecodeError:
						print(f"Skipping invalid JSON line in {jsonFile}")
						continue
					batch.append(obj)
					if len(batch) >= batchSize:
						coll.insert_many(batch)
						batch = []
				if batch:
					coll.insert_many(batch)
		except Exception as e:
			print(f"Failed to import {jsonFile}: {e}")


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

