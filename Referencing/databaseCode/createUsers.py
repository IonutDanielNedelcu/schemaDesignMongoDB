import os
import glob
import json
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

from connection import connectToMongoDB, closeConnection


def is_valid_objectid(s):
    try:
        ObjectId(str(s))
        return True
    except Exception:
        return False


def load_users_json(json_dir):
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


def ensure_address(addr, db):
    # prefer matching by fullAddress when available
    full = addr.get("fullAddress") if isinstance(addr, dict) else None
    if full:
        found = db.addresses.find_one({"fullAddress": full}, {"_id": 1})
        if found:
            return found["_id"]

    # try to find by combination of fields
    query = {}
    for k in ("street", "city", "county", "zipCode", "country", "fullAddress"):
        v = addr.get(k) if isinstance(addr, dict) else None
        if v:
            query[k] = v

    if query:
        found = db.addresses.find_one(query, {"_id": 1})
        if found:
            return found["_id"]

    # insert minimal address doc
    to_insert = {}
    if isinstance(addr, dict):
        for k, v in addr.items():
            to_insert[k] = v
    else:
        to_insert["fullAddress"] = str(addr)

    res = db.addresses.insert_one(to_insert)
    return res.inserted_id


def create_shopping_cart_items_for_user(user, db):
    created_ids = []
    cart = user.get("shoppingCart") or []
    for ci in cart:
        item = {}
        if ci.get("_id") and is_valid_objectid(ci.get("_id")):
            item["_id"] = ObjectId(ci.get("_id"))
        else:
            item["_id"] = ObjectId()

        # resolve productId
        productIdVal = ci.get("productId") or ci.get("product_id") or ci.get("product") or ci.get("sku")
        productObjectId = None
        if productIdVal:
            if is_valid_objectid(productIdVal):
                productObjectId = ObjectId(productIdVal)
            else:
                prod = db.products.find_one({"sku": productIdVal}, {"_id": 1})
                if prod:
                    productObjectId = prod.get("_id")

        if not productObjectId:
            print(f"Warning: could not resolve product for cart item {ci}. Skipping this cart item.")
            continue

        item["productId"] = productObjectId

        try:
            qty = int(ci.get("quantity", 1))
            if qty < 0:
                qty = 1
        except Exception:
            qty = 1
        item["quantity"] = qty

        try:
            res = db.shoppingCartItems.insert_one(item)
            created_ids.append(res.inserted_id)
        except DuplicateKeyError:
            # if duplicate id, fetch the existing
            existing = db.shoppingCartItems.find_one({"_id": item["_id"]}, {"_id": 1})
            if existing:
                created_ids.append(existing["_id"])
        except Exception as e:
            print(f"Error inserting shopping cart item {item}: {e}")

    return created_ids


def main():
    script_dir = os.path.dirname(__file__)
    json_dir = os.path.normpath(os.path.join(script_dir, '..', '..', 'Embedding', 'databaseCode', 'JsonUsers'))

    mongoClient, db = connectToMongoDB()
    if mongoClient is None or db is None:
        print("Failed to connect to MongoDB. Aborting.")
        return

    created_users = 0
    for user in load_users_json(json_dir):
        user_doc = {}
        if user.get("_id") and is_valid_objectid(user.get("_id")):
            user_doc["_id"] = ObjectId(user.get("_id"))
        else:
            user_doc["_id"] = ObjectId()

        user_doc["username"] = user.get("username")
        user_doc["email"] = user.get("email")

        # addresses -> array of ObjectId
        addr_ids = []
        for addr in user.get("addresses", []):
            try:
                aid = ensure_address(addr, db)
                if aid:
                    addr_ids.append(aid)
            except Exception as e:
                print(f"Error processing address {addr} for user {user.get('username')}: {e}")

        user_doc["addresses"] = addr_ids

        # shoppingCart -> create shoppingCartItems and collect their ids
        try:
            cart_ids = create_shopping_cart_items_for_user(user, db)
        except Exception as e:
            print(f"Error creating shopping cart items for user {user.get('username')}: {e}")
            cart_ids = []

        user_doc["shoppingCart"] = cart_ids

        try:
            db.users.insert_one(user_doc)
            created_users += 1
        except DuplicateKeyError:
            # update existing user with addresses and shoppingCart
            db.users.update_one({"_id": user_doc["_id"]}, {"$set": {"addresses": user_doc["addresses"], "shoppingCart": user_doc["shoppingCart"]}})
            print(f"Updated existing user {user_doc['username']}")
        except Exception as e:
            print(f"Error inserting user {user_doc.get('username')}: {e}")

    print(f"Finished. Created or updated {created_users} users in 'users' collection")
    closeConnection(mongoClient)


if __name__ == "__main__":
    main()
