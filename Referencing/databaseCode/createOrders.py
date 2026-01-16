import os
import glob
import json
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


def loadOrdersJsonFiles(jsonDir):
    files = glob.glob(os.path.join(jsonDir, "*.json"))
    for fp in files:
        with open(fp, "r", encoding="utf-8") as fh:
            try:
                data = json.load(fh)
            except Exception as e:
                print(f"Skipping {fp}: could not parse JSON ({e})")
                continue

            if isinstance(data, list):
                for o in data:
                    yield o
            elif isinstance(data, dict):
                yield data


def parseOrderDate(dtStr):
    if not dtStr:
        return None
    try:
        return datetime.fromisoformat(dtStr)
    except Exception:
        try:
            # fallback: try to parse date portion
            return datetime.strptime(dtStr.split("T")[0], "%Y-%m-%d")
        except Exception:
            return None


def ensureAddress(addrObj, db):
    if not addrObj or not isinstance(addrObj, dict):
        return None

    full = addrObj.get("fullAddress")
    if full:
        found = db.addresses.find_one({"fullAddress": full}, {"_id": 1})
        if found:
            return found["_id"]

    query = {}
    for k in ("street", "city", "county", "zipCode", "country", "fullAddress"):
        v = addrObj.get(k)
        if v:
            query[k] = v

    if query:
        found = db.addresses.find_one(query, {"_id": 1})
        if found:
            return found["_id"]

    # insert address
    toInsert = {k: v for k, v in addrObj.items() if v is not None}
    if not toInsert and full:
        toInsert = {"fullAddress": full}

    res = db.addresses.insert_one(toInsert)
    return res.inserted_id


def ensureUser(customerSnapshot, db):
    if not customerSnapshot or not isinstance(customerSnapshot, dict):
        return None

    # try by _id
    cid = customerSnapshot.get("_id")
    if cid and isValidObjectId(cid):
        existing = db.users.find_one({"_id": ObjectId(cid)}, {"_id": 1})
        if existing:
            return existing["_id"]

    # try by email
    email = customerSnapshot.get("email")
    if email:
        existing = db.users.find_one({"email": email}, {"_id": 1})
        if existing:
            return existing["_id"]

    # create user doc (with addresses resolved)
    userDoc = {}
    if cid and isValidObjectId(cid):
        userDoc["_id"] = ObjectId(cid)
    else:
        userDoc["_id"] = ObjectId()

    userDoc["username"] = customerSnapshot.get("username")
    userDoc["email"] = customerSnapshot.get("email")

    addrIds = []
    for addr in customerSnapshot.get("addresses", []):
        try:
            aId = ensureAddress(addr, db)
            if aId:
                addrIds.append(aId)
        except Exception as e:
            print(f"Warning: could not ensure address for user {userDoc.get('username')}: {e}")

    userDoc["addresses"] = addrIds
    userDoc["shoppingCart"] = []

    try:
        db.users.insert_one(userDoc)
        return userDoc["_id"]
    except Exception:
        # if insert fails for duplicate key, try to fetch
        existing = None
        if email:
            existing = db.users.find_one({"email": email}, {"_id": 1})
        if existing:
            return existing["_id"]
        return None


def buildOrderDoc(order, db):
    doc = {}
    # id
    oid = order.get("_id")
    if oid and isValidObjectId(oid):
        doc["_id"] = ObjectId(oid)
    else:
        doc["_id"] = ObjectId()

    doc["orderDate"] = parseOrderDate(order.get("orderDate"))
    doc["total"] = order.get("total")
    doc["status"] = order.get("status")

    # userId from customerSnapshot
    customer = order.get("customerSnapshot") or {}
    userId = None
    if customer:
        cid = customer.get("_id")
        if cid and isValidObjectId(cid):
            userId = ObjectId(cid)
            # ensure user exists
            if not db.users.find_one({"_id": userId}, {"_id": 1}):
                # create minimal user
                ensureUser(customer, db)
        else:
            userId = ensureUser(customer, db)

    doc["userId"] = userId

    # shipping address
    shipDetails = order.get("shippingDetails") or {}
    shipAddr = shipDetails.get("address") if isinstance(shipDetails, dict) else None
    shippingAddressId = ensureAddress(shipAddr, db) if shipAddr else None

    doc["shippingAddressId"] = shippingAddressId

    # shippingDetails object
    shipping = {}
    if isinstance(shipDetails, dict):
        shipping["method"] = shipDetails.get("method")
        shipping["trackingCode"] = shipDetails.get("trackingCode")
    doc["shippingDetails"] = shipping

    return doc


def main():
    scriptDir = os.path.dirname(__file__)
    jsonDir = os.path.normpath(os.path.join(scriptDir, '..', '..', 'Embedding', 'databaseCode', 'JsonOrders'))

    mongoClient, db = connectToMongoDB()
    if mongoClient is None or db is None:
        print("Failed to connect to MongoDB. Aborting.")
        return

    ordersToInsert = []
    countFiles = 0
    for order in loadOrdersJsonFiles(jsonDir):
        countFiles += 1
        try:
            doc = buildOrderDoc(order, db)
            ordersToInsert.append(doc)
        except Exception as e:
            print(f"Skipping order due to error: {e}")

    total = len(ordersToInsert)
    print(f"Collected {total} orders from ~{countFiles} files")

    if total == 0:
        closeConnection(mongoClient)
        return

    batchSize = 200
    inserted = 0
    for i in range(0, total, batchSize):
        batch = ordersToInsert[i:i+batchSize]
        try:
            res = db.orders.insert_many(batch, ordered=False)
            inserted += len(res.inserted_ids)
            print(f"Inserted batch {i//batchSize + 1}: {len(res.inserted_ids)} orders (total inserted: {inserted})")
        except BulkWriteError as bwe:
            print(f"BulkWriteError on batch {i//batchSize + 1}: {getattr(bwe, 'details', bwe)}")
        except Exception as e:
            print(f"Error inserting batch {i//batchSize + 1}: {e}")

    print(f"Finished. Inserted (approx) {inserted} orders into 'orders' collection")
    closeConnection(mongoClient)


if __name__ == "__main__":
    main()
