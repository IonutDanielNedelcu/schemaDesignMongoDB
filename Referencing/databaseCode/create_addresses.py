"""Create `addresses` collection from Embedding user exports.

Each address follows `collectionsStructures/addressesStructure.json`:
  - `_id`, `street`, `city`, `county`, `zipCode`, `country`, `fullAddress`.

This script reads all JSON files under Embedding/databaseCode/JsonUsers
and extracts the `addresses` arrays. It inserts unique `fullAddress`
documents into Referencing `addresses` collection.
"""

import json
from pathlib import Path
from typing import List

from bson import ObjectId
from pymongo.errors import DuplicateKeyError, BulkWriteError

from connection import connectToMongoDB, closeConnection


BASE_DIR = Path(__file__).resolve().parents[2]
EMBEDDING_USERS_DIR = BASE_DIR / "Embedding" / "databaseCode" / "JsonUsers"


def load_addresses(src_dir: Path) -> List[dict]:
    addrs: List[dict] = []
    if not src_dir.exists():
        print(f"Embedding JSON users dir not found: {src_dir}")
        return addrs

    for p in sorted(src_dir.glob("*.json")):
        try:
            with p.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)
            docs = payload if isinstance(payload, list) else [payload]
            for u in docs:
                for a in (u.get("addresses") or []):
                    addr = {
                        "street": a.get("street"),
                        "city": a.get("city"),
                        "county": a.get("county"),
                        "zipCode": a.get("zipcode") or a.get("zipCode"),
                        "country": a.get("country"),
                        "fullAddress": a.get("fullAddress")
                    }
                    addrs.append(addr)
        except Exception as exc:
            print(f"Error reading {p.name}: {exc}")

    return addrs


def main():
    client, db = connectToMongoDB()
    if client is None or db is None:
        print("Failed to connect to Referencing DB. Aborting.")
        return

    try:
        addresses = load_addresses(EMBEDDING_USERS_DIR)
        print(f"Loaded {len(addresses)} address entries from Embedding JSONs")

        coll = db["addresses"]
        try:
            coll.create_index([("fullAddress", 1)], unique=True)
        except Exception:
            pass

        batch = []
        batch_size = 200
        inserted = 0
        total = len(addresses)

        for idx, a in enumerate(addresses, start=1):
            doc = {"_id": ObjectId(), **a}
            batch.append(doc)
            if len(batch) >= batch_size:
                try:
                    coll.insert_many(batch, ordered=False)
                    inserted += len(batch)
                except BulkWriteError:
                    # duplicates may exist; ignore
                    pass
                except Exception as exc:
                    print(f"Batch insert error at idx {idx}: {exc}")
                batch = []
                print(f"Progress: inserted {inserted}/{total}")

        if batch:
            try:
                coll.insert_many(batch, ordered=False)
                inserted += len(batch)
            except BulkWriteError:
                pass

        print(f"Inserted {inserted} addresses into 'addresses' collection")

    finally:
        closeConnection(client)


if __name__ == '__main__':
    main()
