"""Populate `products` collection following `productsStructure.json`.

Reads all JSON files from Embedding/databaseCode/JsonProducts and inserts
documents into `products` collection with fields:
  - `_id` (ObjectId)
  - `name`, `sku`, `price` (Number), `stock`
  - `vendorId` (ObjectId) — resolved from existing `vendors` collection
  - `mainCategoryId`, `subCategoryId` (ObjectId) — resolved from existing `categories`
  - `details` (copy `description` and `specs` as-is)

This script will NOT create `vendors` or `categories` collections; it only
reads them to resolve references. Missing references are left absent.
"""

import json
from pathlib import Path
from typing import List

from bson import ObjectId
from pymongo.errors import BulkWriteError, DuplicateKeyError

from connection import connectToMongoDB, closeConnection


baseDir = Path(__file__).resolve().parents[2]
embeddingProductsDir = baseDir / "Embedding" / "databaseCode" / "JsonProducts"


def loadProducts(srcDir: Path) -> List[dict]:
    docs: List[dict] = []
    if not srcDir.exists():
        print(f"Embedding JSON products dir not found: {srcDir}")
        return docs

    for p in sorted(srcDir.glob("*.json")):
        try:
            with p.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)
            if isinstance(payload, list):
                docs.extend(payload)
            else:
                docs.append(payload)
        except Exception as exc:
            print(f"Error reading {p.name}: {exc}")

    return docs


def makeObjectId(val):
    try:
        if isinstance(val, ObjectId):
            return val
        if isinstance(val, str) and len(val) == 24:
            return ObjectId(val)
    except Exception:
        pass
    return ObjectId()


def resolveCategoryIds(categoriesColl, catObj):
    """Return (mainId, subId) or (None, None) if not resolvable."""
    if not isinstance(catObj, dict):
        return None, None

    main = catObj.get("main")
    sub = catObj.get("sub")
    mainId = None
    subId = None

    if main:
        mainDoc = categoriesColl.find_one({"name": main, "parentCategoryId": None})
        if mainDoc:
            mainId = mainDoc["_id"]

    if sub:
        # Prefer sub under found main; fallback to any matching name
        if mainId:
            subDoc = categoriesColl.find_one({"name": sub, "parentCategoryId": mainId})
            if subDoc:
                subId = subDoc["_id"]
        if subId is None:
            subDoc = categoriesColl.find_one({"name": sub})
            if subDoc:
                subId = subDoc["_id"]
                if mainId is None and subDoc.get("parentCategoryId"):
                    mainId = subDoc.get("parentCategoryId")

    return mainId, subId


def resolveVendorId(vendorsColl, vendorObj):
    if not isinstance(vendorObj, dict):
        return None
    company = vendorObj.get("companyName")
    email = vendorObj.get("contactEmail")
    if not company and not email:
        return None
    query = {k: v for k, v in (("companyName", company), ("contactEmail", email)) if v}
    doc = vendorsColl.find_one(query)
    return doc["_id"] if doc else None


def buildProduct(src, categoriesColl, vendorsColl):
    prod = {}

    # _id
    rawId = src.get("_id")
    prod["_id"] = makeObjectId(rawId)

    # basic fields
    for f in ("name", "sku", "stock"):
        if f in src:
            prod[f] = src[f]

    # price: keep as number (float) per productsStructure
    if "price" in src:
        try:
            prod["price"] = float(src["price"])
        except Exception:
            prod["price"] = 0.0

    # details: copy description and specs if present
    details = src.get("details")
    if isinstance(details, dict):
        # keep only description and specs as requested
        newDetails = {}
        if "description" in details:
            newDetails["description"] = details["description"]
        if "specs" in details:
            newDetails["specs"] = details["specs"]
        if newDetails:
            prod["details"] = newDetails

    # categories
    mainId, subId = resolveCategoryIds(categoriesColl, src.get("category"))
    if mainId:
        prod["mainCategoryId"] = mainId
    if subId:
        prod["subCategoryId"] = subId

    # vendor
    vId = resolveVendorId(vendorsColl, src.get("vendor"))
    if vId:
        prod["vendorId"] = vId

    return prod


def main():
    client, db = connectToMongoDB()
    if client is None or db is None:
        print("Failed to connect to Referencing database. Aborting.")
        return

    try:
        products = loadProducts(embeddingProductsDir)
        print(f"Loaded {len(products)} products from Embedding JSONs")

        categoriesColl = db["categories"]
        vendorsColl = db["vendors"]
        productsColl = db["products"]

        # ensure sku uniqueness
        try:
            productsColl.create_index([("sku", 1)], unique=True)
        except Exception:
            pass

        batch = []
        batchSize = 200
        inserted = 0
        total = len(products)

        for idx, src in enumerate(products, start=1):
            doc = buildProduct(src, categoriesColl, vendorsColl)
            batch.append(doc)
            if len(batch) >= batchSize:
                try:
                    productsColl.insert_many(batch, ordered=False)
                    inserted += len(batch)
                except BulkWriteError as bwe:
                    # count successful inserts if possible
                    inserted += sum(1 for err in bwe.details.get("writeErrors", []) if err.get("code") != 11000)
                except Exception as exc:
                    print(f"Batch insert error at idx {idx}: {exc}")
                batch = []
                print(f"Progress: inserted {inserted}/{total}")

        if batch:
            try:
                productsColl.insert_many(batch, ordered=False)
                inserted += len(batch)
            except BulkWriteError:
                pass

        print(f"Inserted {inserted} products into 'products' collection")

    finally:
        closeConnection(client)


if __name__ == '__main__':
    main()
"""Populate Referencing `products` using exported Embedding JSONs.

Maps embedding `category` and `vendor` to separate collections and
inserts products following `productsStructure.json`.
"""

import json
from decimal import Decimal
from pathlib import Path
from typing import Optional, Tuple

from bson import ObjectId, Decimal128
from pymongo.errors import DuplicateKeyError, BulkWriteError

from connection import connectToMongoDB, closeConnection


baseDir = Path(__file__).resolve().parents[2]
embeddingProductsDir = baseDir / "Embedding" / "databaseCode" / "JsonProducts"
productsStructurePath = Path(__file__).resolve().parent / "collectionsStructures" / "productsStructure.json"


def toDecimal128(value) -> Decimal128:
    try:
        return Decimal128(str(Decimal(value)))
    except Exception:
        return Decimal128("0")


def ensureCategoryCached(cache: dict, coll, name: str, parentId: ObjectId = None) -> Optional[ObjectId]:
    if not name:
        return None
    key = (str(parentId) if parentId is not None else "ROOT", name)
    if key in cache:
        return cache[key]
    query = {"name": name, "parentCategoryId": parentId}
    doc = coll.find_one(query)
    if doc:
        cache[key] = doc["_id"]
        return doc["_id"]
    toInsert = {"_id": ObjectId(), "name": name, "parentCategoryId": parentId}
    res = coll.insert_one(toInsert)
    cache[key] = res.inserted_id
    return res.inserted_id


def ensureVendorCached(cache: dict, coll, vendorObj: dict) -> Optional[ObjectId]:
    if not isinstance(vendorObj, dict):
        return None
    company = vendorObj.get("companyName")
    email = vendorObj.get("contactEmail")
    phone = vendorObj.get("supportPhone")
    if not company:
        return None
    key = (company, email)
    if key in cache:
        return cache[key]
    doc = coll.find_one({"companyName": company, "contactEmail": email})
    if doc:
        cache[key] = doc["_id"]
        return doc["_id"]
    res = coll.insert_one({"_id": ObjectId(), "companyName": company, "contactEmail": email, "supportPhone": phone})
    cache[key] = res.inserted_id
    return res.inserted_id


def loadProductsFromFiles(srcDir: Path):
    products = []
    if not srcDir.exists():
        print(f"Embedding JSON products dir not found: {srcDir}")
        return products

    for path in sorted(srcDir.glob("*.json")):
        try:
            with path.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)
            docs = payload if isinstance(payload, list) else [payload]
            products.extend(docs)
        except Exception as exc:
            print(f"Error reading {path.name}: {exc}")

    return products


def buildProductDocument(src: dict, categoriesMainColl, categoriesSubColl, vendorsColl, mainCache: dict, subCache: dict, vendorCache: dict) -> dict:
    product = {}

    # ID
    rawId = src.get("_id")
    try:
        product["_id"] = ObjectId(rawId) if rawId else ObjectId()
    except Exception:
        product["_id"] = ObjectId()

    # Basic fields
    for field in ("name", "sku", "stock"):
        if field in src:
            product[field] = src[field]

    # Price
    if "price" in src:
        product["price"] = toDecimal128(src["price"])

    # Details (copy as-is)
    if "details" in src:
        product["details"] = src["details"]

    # Categories (use cached ensures into single `categories` collection)
    cat = src.get("category")
    if isinstance(cat, dict):
        main = cat.get("main")
        sub = cat.get("sub")
        if main:
            mainId = ensureCategoryCached(mainCache, categoriesMainColl, main, None)
            product["mainCategoryId"] = mainId
            if sub:
                subId = ensureCategoryCached(subCache, categoriesSubColl, sub, mainId)
                product["subCategoryId"] = subId

    # Vendor (cached)
    vendor = src.get("vendor")
    if vendor:
        vid = ensureVendorCached(vendorCache, vendorsColl, vendor)
        if vid:
            product["vendorId"] = vid

    return product


def main():
    client, db = connectToMongoDB()
    if client is None or db is None:
        print("Failed to connect to Referencing DB. Aborting.")
        return

    try:
        products = loadProductsFromFiles(embeddingProductsDir)
        print(f"Loaded {len(products)} products from Embedding JSONs")
        categoriesColl = db["categories"]
        vendorsColl = db["vendors"]
        productsColl = db["products"]

        # Ensure uniqueness on sku for products
        try:
            productsColl.create_index([("sku", 1)], unique=True)
        except Exception:
            pass

        # Preload caches from DB to avoid repeated lookups
        mainCache = {}
        subCache = {}
        vendorCache = {}

        for doc in categoriesColl.find({}, {"_id": 1, "name": 1, "parentCategoryId": 1}):
            key = (str(doc.get("parentCategoryId")) if doc.get("parentCategoryId") is not None else "ROOT", doc["name"])
            mainCache[key] = doc["_id"]
            # keep same mapping for subCache as well for direct lookup
            subCache[key] = doc["_id"]
        for doc in vendorsColl.find({}, {"_id": 1, "companyName": 1, "contactEmail": 1}):
            vendorCache[(doc.get("companyName"), doc.get("contactEmail"))] = doc["_id"]

        batch = []
        batchSize = 200
        inserted = 0
        total = len(products)
        for idx, src in enumerate(products, start=1):
            doc = buildProductDocument(src, categoriesColl, categoriesColl, vendorsColl, mainCache, subCache, vendorCache)
            batch.append(doc)
            if len(batch) >= batchSize:
                try:
                    productsColl.insert_many(batch, ordered=False)
                    inserted += len(batch)
                except BulkWriteError as bwe:
                    # Some duplicates may be present; count inserted
                    inserted += sum(1 for e in bwe.details.get("writeErrors", []) if e.get("code") != 11000)
                except Exception as exc:
                    print(f"Batch insert error at idx {idx}: {exc}")
                batch = []
                print(f"Progress: inserted {inserted}/{total}")

        # remaining
        if batch:
            try:
                productsColl.insert_many(batch, ordered=False)
                inserted += len(batch)
            except BulkWriteError:
                pass

        print(f"Inserted {inserted} products into Referencing.products")

    finally:
        closeConnection(client)


if __name__ == '__main__':
    main()
