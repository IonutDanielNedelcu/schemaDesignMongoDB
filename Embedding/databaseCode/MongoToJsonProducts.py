import os
import json
from decimal import Decimal
from datetime import datetime
from bson import ObjectId, Decimal128
from connection import connectToMongoDB, closeConnection


def ensureOutputDir(outputDir):
	os.makedirs(outputDir, exist_ok=True)

def makeSerializable(value):
	if isinstance(value, ObjectId):
		return str(value)
	if isinstance(value, Decimal128):
		try:
			return float(value.to_decimal())
		except Exception:
			return str(value)
	if isinstance(value, Decimal):
		try:
			return float(value)
		except Exception:
			return str(value)
	if isinstance(value, datetime):
		return value.isoformat()
	if isinstance(value, dict):
		return {k: makeSerializable(v) for k, v in value.items()}
	if isinstance(value, list):
		return [makeSerializable(v) for v in value]
	return value


def exportProductsToJson(batchSize=50, collectionName='products', outputDir=None, dbName=None):
	if outputDir is None:
		repoRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
		outputDir = os.path.join(repoRoot, 'sharding', 'JsonProducts')

	ensureOutputDir(outputDir)

	mongoClient, db = connectToMongoDB(dbName) if dbName else connectToMongoDB()
	if mongoClient is None or db is None:
		print('Failed to connect to MongoDB. Aborting.')
		return

	try:
		productsCollection = db[collectionName]
		cursor = productsCollection.find()

		batch = []
		fileIndex = 1
		for doc in cursor:
			batch.append(makeSerializable(doc))
			if len(batch) >= batchSize:
				filePath = os.path.join(outputDir, f'products_{fileIndex}.json')
				with open(filePath, 'w', encoding='utf-8') as f:
					json.dump(batch, f, ensure_ascii=False, indent=2)
				print(f'Wrote {len(batch)} products to {filePath}')
				fileIndex += 1
				batch = []

		if batch:
			filePath = os.path.join(outputDir, f'products_{fileIndex}.json')
			with open(filePath, 'w', encoding='utf-8') as f:
				json.dump(batch, f, ensure_ascii=False, indent=2)
			print(f'Wrote {len(batch)} products to {filePath}')

	except Exception as e:
		print(f'Error during export: {e}')

	finally:
		closeConnection(mongoClient)



exportProductsToJson()

