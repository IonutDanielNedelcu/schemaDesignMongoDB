
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()


config = {
	# prefer explicit connection string in env, e.g.:
	# MONGO_CONNECTION_STRING=mongodb://localhost:27111,localhost:27112,localhost:27113/?replicaSet=rs1
	"mongoUri": os.getenv("MONGO_CONNECTION_STRING"),
	"dbName": "eCommerceProjectEmbedding",
	"collections": [
		{"name": "orders", "folder": "JsonOrders"},
		{"name": "products", "folder": "JsonProducts"},
		{"name": "users", "folder": "JsonUsers"},
	],
	# Safety: dry-run unless confirm True
	"confirm": True,
	# batch size for inserts
	"batchSize": 500,
}


def getClient(mongoUri=None):
	mongoUri = mongoUri or config["mongoUri"]
	if not mongoUri:
		# Build mongoUri from setupReplicaSet.py nodes list only
		try:
			base = Path(__file__).parent
			setup_path = base / "setupReplicaSet.py"
			if setup_path.exists():
				import importlib.util
				spec = importlib.util.spec_from_file_location("setupReplicaSet", str(setup_path))
				mod = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(mod)
				if hasattr(mod, 'nodes') and isinstance(mod.nodes, list):
					seeds = [f"localhost:{n['port']}" for n in mod.nodes if isinstance(n, dict) and 'port' in n]
					rset = getattr(mod, 'replicaSetName', getattr(mod, 'REPLICA_SET_NAME', 'rs0'))
					if seeds:
						mongoUri = f"mongodb://{','.join(seeds)}/?replicaSet={rset}"
						print("Built mongoUri from setupReplicaSet.py nodes:", mongoUri)
		except Exception as e:
			print("Could not build mongoUri from setupReplicaSet.py:", e)
	if not mongoUri:
		raise RuntimeError("No mongoUri configured; set MONGO_CONNECTION_STRING in .env or run setupReplicaSet.py")
	return MongoClient(mongoUri, serverSelectionTimeoutMS=5000)


def findPrimaryByDirectConnection(members, timeout=3):
	"""Try to connect directly to each hostPort (localhost:port) with
	directConnection=True and return a client connected to the primary.
	Useful when replica set members report internal container hostnames that
	are not resolvable from the host machine.
	"""
	from pymongo import MongoClient

	for m in members:
		try:
			port = None
			if isinstance(m, dict):
				port = m.get("hostPort") or m.get("port")
			if not port:
				continue
			uri = f"mongodb://localhost:{port}/?directConnection=true"
			print(f"Trying direct connection to {uri} ...")
			client = MongoClient(uri, serverSelectionTimeoutMS=timeout * 1000)
			try:
				# 'hello' works on modern servers; fall back to ismaster key names
				info = None
				try:
					info = client.admin.command("hello")
				except Exception:
					info = client.admin.command("ismaster")

				if info and (info.get("isWritablePrimary") or info.get("ismaster")):
					print(f"Found primary at localhost:{port}")
					return client
			except Exception:
				client.close()
		except Exception as e:
			print(f"Direct connect attempt to localhost:{m.get('hostPort')} failed: {e}")
	return None


# No sharding functions here — we populate a simple replica set


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


def runPopulateReplica():
	print("Configuration:")
	print(config)

	# resolve folder paths relative to Embedding/sharding (where JSON exports live)
	base = Path(__file__).parent.parent / "sharding"
	for c in config["collections"]:
		c["folderPath"] = base / c["folder"]

	if not config["confirm"]:
		print("Dry-run mode. The script would perform the following:")
		print(f"- Connect to replica set: {config['mongoUri'] or '<built-from-containers.json>'}")
		for c in config["collections"]:
			print(f"- Import files from {c['folderPath']} into {config['dbName']}.{c['name']}")
		print("To actually run, set config['confirm'] = True or set env var POPULATE_REPLICA_CONFIRM=1 and re-run.")
		return

	client = None
	try:
		client = getClient()
		client.admin.command("ping")
	except Exception as e:
		print(f"Could not connect to replica set (seed URI attempt failed): {e}")
		# fallback: try direct connections to localhost:hostPort to discover primary
		try:
				# use setupReplicaSet.py nodes list for direct-connection fallback
				setup_path = Path(__file__).parent / "setupReplicaSet.py"
				if setup_path.exists():
					try:
						import importlib.util
						spec = importlib.util.spec_from_file_location("setupReplicaSet", str(setup_path))
						mod = importlib.util.module_from_spec(spec)
						spec.loader.exec_module(mod)
						if hasattr(mod, 'nodes') and isinstance(mod.nodes, list):
							members = mod.nodes
							client = findPrimaryByDirectConnection(members, timeout=3)
							if client:
								print("Connected directly to primary via setupReplicaSet.py nodes")
							else:
								print("Direct-connection fallback via setupReplicaSet.py did not find a primary. Aborting.")
								return
					except Exception as e:
						print("Failed to read setupReplicaSet.py for direct-connection fallback:", e)
						return
				else:
					print("No setupReplicaSet.py found for direct-connection fallback. Aborting.")
					return
		except Exception as e2:
			print(f"Direct-connection fallback error: {e2}")
			return

	try:
		for c in config["collections"]:
			importJsonFolder(client, config["dbName"], c["name"], c["folderPath"], batchSize=config["batchSize"])

	finally:
		if client:
			client.close()


if __name__ == "__main__":
	# allow enabling confirm via env var for convenience
	if os.getenv("POPULATE_REPLICA_CONFIRM") in ("1", "true", "True"):
		config["confirm"] = True
	runPopulateReplica()

