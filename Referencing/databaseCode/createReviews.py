import os
import glob
import json
import re
from datetime import datetime
from bson.objectid import ObjectId
from pymongo.errors import BulkWriteError

from connection import connectToMongoDB, closeConnection


def isValidObjectId(val):
    try:
        ObjectId(str(val))
        return True
    except Exception:
        return False


def loadProductsJsonFiles(jsonDir):
    files = glob.glob(os.path.join(jsonDir, "*.json"))
    for fp in files:
        with open(fp, "r", encoding="utf-8") as fh:
            try:
                data = json.load(fh)
            except Exception as e:
                print(f"Skipping {fp}: could not parse JSON ({e})")
                continue

            if isinstance(data, list):
                for p in data:
                    yield p
            elif isinstance(data, dict):
                yield data


def parseDate(dateStr):
    if not dateStr:
        return None
    try:
        return datetime.fromisoformat(dateStr)
    except Exception:
        try:
            return datetime.strptime(dateStr.split("T")[0], "%Y-%m-%d")
        except Exception:
            return None


def resolveUserIdByDisplayName(displayName, db):
    if not displayName:
        return None

    # exact match first
    found = db.users.find_one({"username": displayName}, {"_id": 1})
    if found:
        return found["_id"]

    # case-insensitive exact
    try:
        regex = re.compile(rf'^{re.escape(displayName)}$', re.IGNORECASE)
        found = db.users.find_one({"username": regex}, {"_id": 1})
        if found:
            return found["_id"]
    except Exception:
        pass

    # partial match - try contains
    try:
        regex = re.compile(re.escape(displayName), re.IGNORECASE)
        found = db.users.find_one({"username": regex}, {"_id": 1})
        if found:
            return found["_id"]
    except Exception:
        pass

    print(f"Warning: user with displayName '{displayName}' not found in users collection")
    return None


def resolveProductId(product, db):
    # product may be dict with _id or sku
    if not product or not isinstance(product, dict):
        return None

    pid = product.get("_id")
    if pid and isValidObjectId(pid):
        return ObjectId(pid)

    sku = product.get("sku")
    if sku:
        found = db.products.find_one({"sku": sku}, {"_id": 1})
        if found:
            return found["_id"]

    # fallback: try to find product by name
    name = product.get("name")
    if name:
        found = db.products.find_one({"name": name}, {"_id": 1})
        if found:
            return found["_id"]

    return None


def buildReviewDocsFromProduct(product, db):
    reviews = product.get("reviews") or []
    prodId = None
    # product might be the product doc itself (from JSON) with _id
    if product.get("_id") and isValidObjectId(product.get("_id")):
        prodId = ObjectId(product.get("_id"))
    else:
        # try to resolve via sku or name
        prodId = resolveProductId(product, db)

    docs = []
    for r in reviews:
        doc = {}
        # id
        if r.get("_id") and isValidObjectId(r.get("_id")):
            doc["_id"] = ObjectId(r.get("_id"))
        else:
            doc["_id"] = ObjectId()

        # productId
        if prodId:
            doc["productId"] = prodId
        else:
            # try to resolve from nested product reference inside review
            nested = r.get("product")
            pId = resolveProductId(nested or product, db)
            if pId:
                doc["productId"] = pId
            else:
                print(f"Warning: could not resolve productId for review {r}. Skipping.")
                continue

        # userId via userDisplayName
        userDisplay = r.get("userDisplayName") or r.get("user") or r.get("userDisplay")
        userId = resolveUserIdByDisplayName(userDisplay, db) if userDisplay else None
        doc["userId"] = userId

        # rating
        try:
            ratingVal = r.get("rating")
            rating = float(ratingVal) if ratingVal is not None else None
        except Exception:
            rating = None
        doc["rating"] = rating

        # comment
        comment = r.get("comment") or r.get("text") or r.get("review")
        doc["comment"] = comment

        # date
        doc["date"] = parseDate(r.get("date") or r.get("createdAt") or r.get("timestamp"))

        docs.append(doc)

    return docs


def main():
    scriptDir = os.path.dirname(__file__)
    jsonDir = os.path.normpath(os.path.join(scriptDir, '..', '..', 'Embedding', 'databaseCode', 'JsonProducts'))

    mongoClient, db = connectToMongoDB()
    if mongoClient is None or db is None:
        print("Failed to connect to MongoDB. Aborting.")
        return

    allDocs = []
    fileCount = 0
    for product in loadProductsJsonFiles(jsonDir):
        fileCount += 1
        docs = buildReviewDocsFromProduct(product, db)
        if docs:
            allDocs.extend(docs)

    total = len(allDocs)
    print(f"Collected {total} reviews from ~{fileCount} product files")

    if total == 0:
        closeConnection(mongoClient)
        return

    batchSize = 200
    inserted = 0
    for i in range(0, total, batchSize):
        batch = allDocs[i:i+batchSize]
        try:
            res = db.reviews.insert_many(batch, ordered=False)
            inserted += len(res.inserted_ids)
            print(f"Inserted batch {i//batchSize + 1}: {len(res.inserted_ids)} reviews (total inserted: {inserted})")
        except BulkWriteError as bwe:
            print(f"BulkWriteError on batch {i//batchSize + 1}: {getattr(bwe, 'details', bwe)}")
        except Exception as e:
            print(f"Error inserting batch {i//batchSize + 1}: {e}")

    print(f"Finished. Inserted (approx) {inserted} documents into 'reviews' collection")
    closeConnection(mongoClient)


if __name__ == "__main__":
    main()
