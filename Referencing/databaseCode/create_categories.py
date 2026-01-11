"""Create a `categories` collection in the Referencing database.

This script scans exported product JSON files (from the Embedding part of
the project), extracts distinct category pairs `(main, sub)` and inserts
them into a single `categories` collection using the structure:

    {
        "_id": ObjectId,
        "name": String,
        "parentCategoryId": ObjectId or None
    }

Main categories are inserted with `parentCategoryId = None` and sub
categories are inserted with `parentCategoryId` pointing to the parent's
`_id`.
"""

import json
from pathlib import Path
from typing import Optional, Set, Tuple, Dict

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from connection import connectToMongoDB, closeConnection


# Path to exported product JSON files from the Embedding project
EMBEDDING_PRODUCTS_DIR = (
    Path(__file__).resolve().parents[2] / "Embedding" / "databaseCode" / "JsonProducts"
)


def collect_categories(json_dir: Path) -> Set[Tuple[str, Optional[str]]]:
    """Collect unique (main, sub) category tuples from JSON files.

    Returns a set of tuples where `sub` can be None if not present.
    """
    categories: Set[Tuple[str, Optional[str]]] = set()

    if not json_dir.exists():
        print(f'Embedding JSON directory not found: {json_dir}')
        return categories

    for json_path in sorted(json_dir.glob("*.json")):
        try:
            with json_path.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)

            # Expecting either a list of documents or a single document
            documents = payload if isinstance(payload, list) else [payload]

            for doc in documents:
                category = doc.get("category")
                if isinstance(category, dict):
                    main = category.get("main")
                    sub = category.get("sub")
                    if main:
                        categories.add((main, sub if sub else None))

        except Exception as exc:
            print(f'Error reading {json_path.name}: {exc}')

    return categories


def insert_categories(categories: Set[Tuple[str, Optional[str]]], db_name: Optional[str] = None, collection_name: str = "categories") -> None:
    """Insert category documents into the Referencing database.

    This builds main category documents (parentCategoryId=None) and then
    subcategory documents that reference their parent's `_id`.
    """
    if not categories:
        print("No categories found to insert.")
        return

    client, db = connectToMongoDB(db_name) if db_name else connectToMongoDB()
    if client is None or db is None:
        print("Failed to connect to Referencing database. Aborting.")
        return

    try:
        coll = db[collection_name]
        # Ensure uniqueness on (name, parentCategoryId)
        try:
            coll.create_index([("name", 1), ("parentCategoryId", 1)], unique=True)
        except Exception:
            pass

        # First, create main categories and keep a map name -> _id
        main_map: Dict[str, ObjectId] = {}
        mains = sorted({m for (m, _) in categories})
        inserted_main = 0
        print(f"Creating {len(mains)} main categories...")
        for main in mains:
            try:
                res = coll.insert_one({"_id": ObjectId(), "name": main, "parentCategoryId": None})
                main_map[main] = res.inserted_id
                inserted_main += 1
            except DuplicateKeyError:
                existing = coll.find_one({"name": main, "parentCategoryId": None})
                if existing:
                    main_map[main] = existing["_id"]
                continue
            except Exception as exc:
                print(f"Insert error for main category {main!r}: {exc}")

        # Then insert subcategories linking to parents
        subs = sorted([(m, s) for (m, s) in categories if s])
        inserted_sub = 0
        print(f"Creating {len(subs)} subcategories...")
        for main, sub in subs:
            parent_id = main_map.get(main)
            if not parent_id:
                # Try to find parent in DB in case it existed already
                parent_doc = coll.find_one({"name": main, "parentCategoryId": None})
                if parent_doc:
                    parent_id = parent_doc["_id"]
                    main_map[main] = parent_id
                else:
                    print(f"Warning: parent category {main!r} not found for sub {sub!r}; skipping")
                    continue

            try:
                coll.insert_one({"_id": ObjectId(), "name": sub, "parentCategoryId": parent_id})
                inserted_sub += 1
            except DuplicateKeyError:
                continue
            except Exception as exc:
                print(f"Insert error for subcategory {sub!r} under {main!r}: {exc}")

        print(f"Inserted {inserted_main} main and {inserted_sub} sub categories into '{collection_name}'")

    finally:
        closeConnection(client)


def main() -> None:
    """Main entry point: collect categories and insert into DB."""
    print(f"Scanning product JSON files in: {EMBEDDING_PRODUCTS_DIR}")
    cats = collect_categories(EMBEDDING_PRODUCTS_DIR)
    print(f"Found {len(cats)} unique (main, sub) category tuples")
    for main, sub in sorted(cats):
        print("-", main, "|", sub)

    insert_categories(cats)


if __name__ == "__main__":
    main()
