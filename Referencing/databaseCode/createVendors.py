import json
from pathlib import Path
from typing import Optional, Set, Tuple
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from connection import connectToMongoDB, closeConnection


# Path to exported product JSON files from the Embedding project
embeddingProductsDir = (
    Path(__file__).resolve().parents[2] / "Embedding" / "databaseCode" / "JsonProducts"
)


def collectVendors(jsonDir: Path) -> Set[Tuple[str, Optional[str], Optional[str]]]:
    # Collect unique vendors as tuples (companyName, contactEmail, supportPhone)
    vendorsSet = set()

    if not jsonDir.exists():
        print(f'Embedding JSON directory not found: {jsonDir}')
        return vendorsSet

    for jsonPath in sorted(jsonDir.glob("*.json")):
        try:
            with jsonPath.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)

            documents = payload if isinstance(payload, list) else [payload]
            for doc in documents:
                vendor = doc.get("vendor")
                if isinstance(vendor, dict):
                    companyName = vendor.get("companyName")
                    contactEmail = vendor.get("contactEmail")
                    supportPhone = vendor.get("supportPhone")
                    if companyName:
                        vendorsSet.add((companyName, contactEmail if contactEmail else None, supportPhone if supportPhone else None))

        except Exception as exc:
            print(f'Error reading {jsonPath.name}: {exc}')

    return vendorsSet


def insertVendors(vendorsSet: Set[Tuple[str, Optional[str], Optional[str]]], dbName: Optional[str] = None, collectionName: str = "vendors") -> None:
    # Insert vendor documents into Referencing database
    if not vendorsSet:
        print("No vendors found to insert.")
        return

    client, db = connectToMongoDB(dbName) if dbName else connectToMongoDB()
    if client is None or db is None:
        print("Failed to connect to Referencing database. Aborting.")
        return

    try:
        collection = db[collectionName]
        # Ensure uniqueness on companyName + contactEmail
        try:
            collection.create_index([("companyName", 1), ("contactEmail", 1)], unique=True)
        except Exception:
            pass

        inserted = 0
        for companyName, contactEmail, supportPhone in sorted(vendorsSet):
            doc = {"_id": ObjectId(), "companyName": companyName, "contactEmail": contactEmail, "supportPhone": supportPhone}
            try:
                collection.insert_one(doc)
                inserted += 1
            except DuplicateKeyError:
                continue
            except Exception as exc:
                print(f'Insert error for {companyName!r}/{contactEmail!r}: {exc}')

        print(f"Inserted {inserted} vendors into '{collectionName}'")

    finally:
        closeConnection(client)


def main() -> None:
    print(f"Scanning product JSON files in: {embeddingProductsDir}")
    vendorsSet = collectVendors(embeddingProductsDir)
    print(f"Found {len(vendorsSet)} unique vendors")
    for companyName, contactEmail, supportPhone in sorted(vendorsSet):
        print("-", companyName, "|", contactEmail, "|", supportPhone)

    insertVendors(vendorsSet)


if __name__ == "__main__":
    main()
