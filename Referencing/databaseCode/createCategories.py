import json
from pathlib import Path
from typing import Optional, Set, Tuple, Dict
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from connection import connectToMongoDB, closeConnection


# Path to exported product JSON files from the Embedding project
embeddingProductsDir = (
    Path(__file__).resolve().parents[2] / "Embedding" / "databaseCode" / "JsonProducts"
)


def collectCategories(jsonDir: Path) -> Set[Tuple[str, Optional[str]]]:
    # Collect unique (main, sub) category tuples from JSON files
    categories: Set[Tuple[str, Optional[str]]] = set()

    if not jsonDir.exists():
        print(f'Embedding JSON directory not found: {jsonDir}')
        return categories

    for jsonPath in sorted(jsonDir.glob("*.json")):
        try:
            with jsonPath.open("r", encoding="utf-8") as fh:
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
            print(f'Error reading {jsonPath.name}: {exc}')

    return categories


def insertCategories(categories: Set[Tuple[str, Optional[str]]], dbName: Optional[str] = None, collectionName: str = "categories") -> None:
    # This builds main category documents (parentCategoryId=None) and then
    # subcategory documents that reference their parent's `_id`
    if not categories:
        print("No categories found to insert.")
        return

    client, db = connectToMongoDB(dbName) if dbName else connectToMongoDB()
    if client is None or db is None:
        print("Failed to connect to Referencing database. Aborting.")
        return

    try:
        collection = db[collectionName]
        # Ensure uniqueness on (name, parentCategoryId)
        try:
            collection.create_index([("name", 1), ("parentCategoryId", 1)], unique=True)
        except Exception:
            pass

        # First, create main categories and keep a map name -> _id
        mainMap: Dict[str, ObjectId] = {}
        mains = sorted({m for (m, _) in categories})
        insertedMain = 0
        print(f"Creating {len(mains)} main categories...")
        for main in mains:
            try:
                res = collection.insert_one({"_id": ObjectId(), "name": main, "parentCategoryId": None})
                mainMap[main] = res.inserted_id
                insertedMain += 1
            except DuplicateKeyError:
                existing = collection.find_one({"name": main, "parentCategoryId": None})
                if existing:
                    mainMap[main] = existing["_id"]
                continue
            except Exception as exc:
                print(f"Insert error for main category {main!r}: {exc}")

        # Then insert subcategories linking to parents
        subs = sorted([(m, s) for (m, s) in categories if s])
        insertedSub = 0
        print(f"Creating {len(subs)} subcategories...")
        for main, sub in subs:
            parent_id = mainMap.get(main)
            if not parent_id:
                # Try to find parent in DB in case it existed already
                parentDoc = collection.find_one({"name": main, "parentCategoryId": None})
                if parentDoc:
                    parent_id = parentDoc["_id"]
                    mainMap[main] = parent_id
                else:
                    print(f"Warning: parent category {main!r} not found for sub {sub!r}; skipping")
                    continue

            try:
                collection.insert_one({"_id": ObjectId(), "name": sub, "parentCategoryId": parent_id})
                insertedSub += 1
            except DuplicateKeyError:
                continue
            except Exception as exc:
                print(f"Insert error for subcategory {sub!r} under {main!r}: {exc}")

        print(f"Inserted {insertedMain} main and {insertedSub} sub categories into '{collectionName}'")

    finally:
        closeConnection(client)


def main() -> None:
    # Main entry point: collect categories and insert into DB
    print(f"Scanning product JSON files in: {embeddingProductsDir}")
    cats = collectCategories(embeddingProductsDir)
    print(f"Found {len(cats)} unique (main, sub) category tuples")
    for main, sub in sorted(cats):
        print("-", main, "|", sub)

    insertCategories(cats)


if __name__ == "__main__":
    main()
