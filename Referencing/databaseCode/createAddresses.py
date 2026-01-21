import json
from pathlib import Path
from typing import List
from bson import ObjectId
from pymongo.errors import DuplicateKeyError, BulkWriteError
from connection import connectToMongoDB, closeConnection


embeddingUsersDir = (
    Path(__file__).resolve().parents[2] / "Embedding" / "databaseCode" / "JsonUsers"
)


def loadAddresses(srcDir: Path) -> List[dict]:
    addressesList: List[dict] = []
    if not srcDir.exists():
        print(f"Embedding JSON users dir not found: {srcDir}")
        return addressesList

    for p in sorted(srcDir.glob("*.json")):
        try:
            with p.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)
            docs = payload if isinstance(payload, list) else [payload]
            for u in docs:
                for a in (u.get("addresses") or []):
                    addrObj = {
                        "street": a.get("street"),
                        "city": a.get("city"),
                        "county": a.get("county"),
                        "zipCode": a.get("zipcode") or a.get("zipCode"),
                        "country": a.get("country"),
                        "fullAddress": a.get("fullAddress")
                    }
                    addressesList.append(addrObj)
        except Exception as exc:
            print(f"Error reading {p.name}: {exc}")

    return addressesList


def main():
    client, db = connectToMongoDB()
    if client is None or db is None:
        print("Failed to connect to Referencing DB. Aborting.")
        return

    try:
        addresses = loadAddresses(embeddingUsersDir)
        print(f"Loaded {len(addresses)} address entries from Embedding JSONs")

        collection = db["addresses"]
        try:
            collection.create_index([("fullAddress", 1)], unique=True)
        except Exception:
            pass

        batch = []
        batchSize = 200
        inserted = 0
        total = len(addresses)

        for idx, addr in enumerate(addresses, start=1):
            doc = {"_id": ObjectId(), **addr}
            batch.append(doc)
            if len(batch) >= batchSize:
                try:
                    collection.insert_many(batch, ordered=False)
                    inserted += len(batch)
                except BulkWriteError:
                    pass
                except Exception as exc:
                    print(f"Batch insert error at idx {idx}: {exc}")
                batch = []
                print(f"Progress: inserted {inserted}/{total}")

        if batch:
            try:
                collection.insert_many(batch, ordered=False)
                inserted += len(batch)
            except BulkWriteError:
                pass

        print(f"Inserted {inserted} addresses into 'addresses' collection")

    finally:
        closeConnection(client)


if __name__ == '__main__':
    main()
