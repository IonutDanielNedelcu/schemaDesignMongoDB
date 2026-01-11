"""Build `vendors` collection in Referencing DB from exported product JSONs.

Scan the JSON files produced by the Embedding scripts, extract unique
vendor objects and insert them into the `vendors` collection.
"""

import json
from pathlib import Path
from typing import Optional, Set, Tuple

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from connection import connectToMongoDB, closeConnection


# Path to exported product JSON files from the Embedding project
EMBEDDING_PRODUCTS_DIR = (
    Path(__file__).resolve().parents[2] / "Embedding" / "databaseCode" / "JsonProducts"
)


def collect_vendors(json_dir: Path) -> Set[Tuple[str, Optional[str], Optional[str]]]:
    """Collect unique vendors as tuples (companyName, contactEmail, supportPhone).

    The contactEmail and supportPhone fields can be None if missing.
    """
    vendors = set()

    if not json_dir.exists():
        print(f'Embedding JSON directory not found: {json_dir}')
        return vendors

    for json_path in sorted(json_dir.glob("*.json")):
        try:
            with json_path.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)

            documents = payload if isinstance(payload, list) else [payload]
            for doc in documents:
                vendor = doc.get("vendor")
                if isinstance(vendor, dict):
                    company = vendor.get("companyName")
                    email = vendor.get("contactEmail")
                    phone = vendor.get("supportPhone")
                    if company:
                        vendors.add((company, email if email else None, phone if phone else None))

        except Exception as exc:
            print(f'Error reading {json_path.name}: {exc}')

    return vendors


def insert_vendors(vendors: Set[Tuple[str, Optional[str], Optional[str]]], db_name: Optional[str] = None, collection_name: str = "vendors") -> None:
    """Insert vendor documents into Referencing database."""
    if not vendors:
        print("No vendors found to insert.")
        return

    client, db = connectToMongoDB(db_name) if db_name else connectToMongoDB()
    if client is None or db is None:
        print("Failed to connect to Referencing database. Aborting.")
        return

    try:
        coll = db[collection_name]
        # Ensure uniqueness on companyName + contactEmail
        try:
            coll.create_index([("companyName", 1), ("contactEmail", 1)], unique=True)
        except Exception:
            pass

        inserted = 0
        for company, email, phone in sorted(vendors):
            doc = {"_id": ObjectId(), "companyName": company, "contactEmail": email, "supportPhone": phone}
            try:
                coll.insert_one(doc)
                inserted += 1
            except DuplicateKeyError:
                continue
            except Exception as exc:
                print(f'Insert error for {company!r}/{email!r}: {exc}')

        print(f"Inserted {inserted} vendors into '{collection_name}'")

    finally:
        closeConnection(client)


def main() -> None:
    print(f"Scanning product JSON files in: {EMBEDDING_PRODUCTS_DIR}")
    vendors = collect_vendors(EMBEDDING_PRODUCTS_DIR)
    print(f"Found {len(vendors)} unique vendors")
    for company, email, phone in sorted(vendors):
        print("-", company, "|", email, "|", phone)

    insert_vendors(vendors)


if __name__ == "__main__":
    main()
