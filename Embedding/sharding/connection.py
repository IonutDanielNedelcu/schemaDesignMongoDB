import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

def connectToMongoDB(dbName="eCommerceProjectEmbedding"):
    try:
        mongoUri = os.getenv("MONGO_CONNECTION_STRING_SHARDING") # using the Docker mongos
        if not mongoUri:
            raise ValueError("MONGO_CONNECTION_STRING_SHARDING not set")
        
        mongoClient = MongoClient(mongoUri, serverSelectionTimeoutMS=5000)
        print("Connection successful")
        
        database = mongoClient[dbName]
        print(f"Connected to database {dbName}")
        
        serverInfo = mongoClient.server_info()
        print(f"MongoDB version: {serverInfo.get('version', 'Unknown')}")
        
        return mongoClient, database
    
    except ConnectionFailure:
        print("Could not connect to server")
        return None, None
    
    except ServerSelectionTimeoutError:
        print("Connection timeout")
        return None, None
    
    except Exception as e:
        print(f"{e}")
        return None, None


def closeConnection(mongoClient):
    if mongoClient:
        mongoClient.close()
        print("Connection closed")


def testConnection():
    print('Trying to connect to database')
    mongoClient, db = connectToMongoDB()

    if mongoClient is not None and db is not None:
        collections = db.list_collection_names()
        if collections:
            print(f"\nDatabase collections: {collections}")
        else:
            print("\nEmpty database. No collections found")

        closeConnection(mongoClient)
    else:
        print("\nConnection failed")


if __name__ == '__main__':
    testConnection()
