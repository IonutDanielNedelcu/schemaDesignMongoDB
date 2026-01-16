import os
import glob
import json
from bson.objectid import ObjectId
from pymongo.errors import BulkWriteError

from connection import connectToMongoDB, closeConnection


def is_valid_objectid(s):
    try:
        ObjectId(str(s))
        return True
    except Exception:
        return False


def loadUsersJsonFiles(json_dir):
    files = glob.glob(os.path.join(json_dir, "*.json"))
    for fp in files:
        with open(fp, "r", encoding="utf-8") as fh:
            try:
                data = json.load(fh)
            except Exception as e:
                print(f"Skipping {fp}: could not parse JSON ({e})")
                continue

            if isinstance(data, list):
                for u in data:
                    yield u
            elif isinstance(data, dict):
                yield data


def buildShoppingCartItemsFromUser(user, db):
    items = []
    cart = user.get("shoppingCart") or []
    for ci in cart:
        # determine _id
        doc = {}
        if ci.get("_id") and is_valid_objectid(ci.get("_id")):
            doc["_id"] = ObjectId(ci.get("_id"))
        else:
            doc["_id"] = ObjectId()

        # resolve productId
        productIdVal = ci.get("productId") or ci.get("product_id") or ci.get("product") or ci.get("sku")
        productObjectId = None
        if productIdVal:
            if is_valid_objectid(productIdVal):
                productObjectId = ObjectId(productIdVal)
            else:
                # assume it's a sku, try to look up in products collection
                prod = db.products.find_one({"sku": productIdVal}, {"_id": 1})
                if prod:
                    productObjectId = prod.get("_id")

        if not productObjectId:
            # cannot resolve product; skip this cart item
            print(f"Warning: could not resolve product for cart item: {ci}. Skipping.")
            continue

        doc["productId"] = productObjectId

        # quantity
        try:
            qty = int(ci.get("quantity", 1))
            if qty < 0:
                qty = 1
        except Exception:
            qty = 1
        doc["quantity"] = qty

        items.append(doc)

    return items


def main():
    script_dir = os.path.dirname(__file__)
    json_dir = os.path.normpath(os.path.join(script_dir, '..', '..', 'Embedding', 'databaseCode', 'JsonUsers'))

    mongoClient, db = connectToMongoDB()
    if mongoClient is None or db is None:
        print("Failed to connect to MongoDB. Aborting.")
        return

    all_items = []
    count_files = 0
    for user in loadUsersJsonFiles(json_dir):
        count_files += 1
        items = buildShoppingCartItemsFromUser(user, db)
        if items:
            all_items.extend(items)

    total = len(all_items)
    print(f"Collected {total} shopping cart items from ~{count_files} user files")

    if total == 0:
        closeConnection(mongoClient)
        return

    # insert in batches
    batch_size = 200
    inserted = 0
    for i in range(0, total, batch_size):
        batch = all_items[i:i+batch_size]
        try:
            res = db.shoppingCartItems.insert_many(batch, ordered=False)
            inserted += len(res.inserted_ids)
            print(f"Inserted batch {i//batch_size + 1}: {len(res.inserted_ids)} items (total inserted: {inserted})")
        except BulkWriteError as bwe:
            # some inserts may have failed due to duplicates
            details = bwe.details if hasattr(bwe, 'details') else bwe
            print(f"BulkWriteError on batch {i//batch_size + 1}: {details}")
        except Exception as e:
            print(f"Error inserting batch {i//batch_size + 1}: {e}")

    print(f"Finished. Inserted (approx) {inserted} shopping cart items into 'shoppingCartItems' collection")

    closeConnection(mongoClient)


if __name__ == "__main__":
    main()
