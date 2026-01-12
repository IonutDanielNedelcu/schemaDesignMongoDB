"""
Connect to a sharded cluster's mongos and run sample queries.

Edit the `config` dict below to change the `mongoUri`, database, collection
and the queries to execute. The script prints concise results for each
query so you can verify the sharded cluster is responding.

Usage: python runQueriesOnShardedCluster.py
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError

load_dotenv()


config = {
    "mongoUri": os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017"),
    "dbName": "eCommerceProjectEmbedding",
    "collectionName": "orders",
    # A small set of example queries to run. Edit or extend as needed.
    "queries": [
        {"name": "countAll", "type": "count", "filter": {}},
        {"name": "findSome", "type": "find", "filter": {}, "limit": 5},
        {
            "name": "topUsersByOrders",
            "type": "aggregate",
            "pipeline": [
                {"$group": {"_id": "$user_id", "orders": {"$sum": 1}}},
                {"$sort": {"orders": -1}},
                {"$limit": 5},
            ],
        },
    ],
}


def getClient(mongoUri):
    client = MongoClient(mongoUri, serverSelectionTimeoutMS=5000)
    return client


def runQuery(client, dbName, collName, q):
    db = client[dbName]
    coll = db[collName]
    qtype = q.get("type")
    try:
        if qtype == "count":
            cnt = coll.count_documents(q.get("filter", {}))
            print(f"{q['name']}: count = {cnt}")

        elif qtype == "find":
            cursor = coll.find(q.get("filter", {})).limit(q.get("limit", 10))
            docs = list(cursor)
            print(f"{q['name']}: returned {len(docs)} documents; sample:")
            for d in docs[:3]:
                print(" -", {k: d.get(k) for k in ("_id", "user_id", "created_at") if k in d})

        elif qtype == "aggregate":
            pipeline = q.get("pipeline", [])
            res = list(coll.aggregate(pipeline))
            print(f"{q['name']}: {len(res)} result(s)")
            for r in res[:5]:
                print(" -", r)

        else:
            print(f"Unknown query type: {qtype}")

    except PyMongoError as e:
        print(f"Query {q.get('name')} failed: {e}")


def main():
    mongoUri = config["mongoUri"]
    print("Connecting to mongos at:", mongoUri)
    try:
        client = getClient(mongoUri)
        client.admin.command("ping")
    except ServerSelectionTimeoutError as e:
        print("Could not connect to mongos:", e)
        return
    except Exception as e:
        print("Connection error:", e)
        return

    try:
        for q in config["queries"]:
            print("---")
            runQuery(client, config["dbName"], config["collectionName"], q)
    finally:
        client.close()


if __name__ == "__main__":
    main()
