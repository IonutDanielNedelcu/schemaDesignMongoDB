import os
import glob
import json
import argparse
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


def loadOrdersJsonFiles_indexed(jsonDir):
    files = sorted(glob.glob(os.path.join(jsonDir, "*.json")))
    for fileIndex, fp in enumerate(files):
        with open(fp, "r", encoding="utf-8") as fh:
            try:
                data = json.load(fh)
            except Exception as e:
                print(f"Skipping {fp}: could not parse JSON ({e})")
                continue

            if isinstance(data, list):
                for orderIndex, o in enumerate(data):
                    yield fileIndex, orderIndex, o, fp
            elif isinstance(data, dict):
                yield fileIndex, 0, data, fp


def resolveProductId(item, db):
    # Accept productId (ObjectId-string), sku, or nested product object
    pid = item.get("productId") or item.get("product_id") or None
    if pid and isValidObjectId(pid):
        return ObjectId(pid)

    # maybe sku
    sku = item.get("sku") or item.get("productSku") or None
    if sku:
        prod = db.products.find_one({"sku": sku}, {"_id": 1, "vendorId": 1})
        if prod:
            return prod.get("_id")

    # nested product
    prodObj = item.get("product")
    if isinstance(prodObj, dict):
        if prodObj.get("_id") and isValidObjectId(prodObj.get("_id")):
            return ObjectId(prodObj.get("_id"))
        if prodObj.get("sku"):
            prod = db.products.find_one({"sku": prodObj.get("sku")}, {"_id": 1})
            if prod:
                return prod.get("_id")

    return None


def resolveVendorIdFromProduct(productId, db):
    if not productId:
        return None
    prod = db.products.find_one({"_id": productId}, {"vendorId": 1})
    if not prod:
        return None
    vendorId = prod.get("vendorId")
    if vendorId and isValidObjectId(vendorId):
        return ObjectId(vendorId)
    return vendorId


def resolveOrderId(order, db):
    oid = order.get("_id")
    if oid and isValidObjectId(oid):
        objId = ObjectId(oid)
        if db.orders.find_one({"_id": objId}, {"_id": 1}):
            return objId
    # fallback: try to find order by orderDate + total + status (parse date to match DB)
    query = {}
    orderDateRaw = order.get("orderDate")
    if orderDateRaw:
        try:
            orderDate = datetime.fromisoformat(orderDateRaw)
            query["orderDate"] = orderDate
        except Exception:
            # keep raw if parse fails
            query["orderDate"] = orderDateRaw
    if order.get("total") is not None:
        query["total"] = order.get("total")
    if order.get("status"):
        query["status"] = order.get("status")

    if query:
        found = db.orders.find_one(query, {"_id": 1})
        if found:
            return found.get("_id")

    # if not found, return None (don't fabricate order id)
    return None


def buildOrderItemDocsFromOrder(order, db, allowMissingOrder=False):
    items = order.get("items") or []
    orderId = resolveOrderId(order, db)
    docs = []

    if orderId is None and not allowMissingOrder:
        # skip entire order if we cannot find matching order
        print(f"Skipping order (no matching order found): {order.get('_id')}")
        return docs

    for it in items:
        doc = {}
        # _id
        if it.get("_id") and isValidObjectId(it.get("_id")):
            doc["_id"] = ObjectId(it.get("_id"))
        else:
            doc["_id"] = ObjectId()

        doc["orderId"] = orderId

        productId = resolveProductId(it, db)
        if not productId:
            print(f"Warning: could not resolve product for order item {it}. Skipping.")
            continue
        doc["productId"] = productId

        # quantity
        try:
            qty = int(it.get("quantity", 1))
            if qty < 0:
                qty = 1
        except Exception:
            qty = 1
        doc["quantity"] = qty

        # vendorId: prefer explicit, else from product
        vId = it.get("vendorId") or it.get("vendor_id") or None
        vendorId = None
        if vId:
            if isValidObjectId(vId):
                vendorId = ObjectId(vId)
            else:
                # if vendor id stored as ObjectId in DB already, resolve safely
                try:
                    vendorId = ObjectId(str(vId))
                except Exception:
                    vendorId = None
        if not vendorId:
            vendorId = resolveVendorIdFromProduct(productId, db)

        if vendorId:
            doc["vendorId"] = vendorId

        docs.append(doc)

    return docs


def main():
    scriptDir = os.path.dirname(__file__)
    jsonDir = os.path.normpath(os.path.join(scriptDir, '..', '..', 'Embedding', 'databaseCode', 'JsonOrders'))

    mongoClient, db = connectToMongoDB()
    if mongoClient is None or db is None:
        print("Failed to connect to MongoDB. Aborting.")
        return

    parser = argparse.ArgumentParser(description="Import order items from JsonOrders with streaming and partial runs")
    parser.add_argument("--max-items", type=int, default=0, help="Maximum number of order items to insert (0 = all)")
    parser.add_argument("--batch-size", type=int, default=200, help="Insert batch size")
    parser.add_argument("--allow-missing-order", action="store_true", help="Allow creating items with no matching orderId (will set orderId to None)")
    parser.add_argument("--reset-progress", action="store_true", help="Reset persisted progress and start from the beginning")
    args = parser.parse_args()

    maxItems = args.max_items
    batchSize = args.batch_size
    allowMissing = args.allow_missing_order

    fileCount = 0
    inserted = 0
    buffer = []
    skippedOrders = 0

    progress_file = os.path.join(scriptDir, ".createOrderItems.progress.json")
    start_file_index = 0
    start_order_index = 0
    if args.reset_progress and os.path.exists(progress_file):
        try:
            os.remove(progress_file)
            print("Progress file removed; starting from the beginning.")
        except Exception as e:
            print(f"Could not remove progress file: {e}")

    if os.path.exists(progress_file):
        try:
            with open(progress_file, "r", encoding="utf-8") as pf:
                pj = json.load(pf)
                start_file_index = int(pj.get("fileIndex", 0))
                start_order_index = int(pj.get("orderIndex", 0))
                print(f"Resuming from fileIndex={start_file_index}, orderIndex={start_order_index}")
        except Exception as e:
            print(f"Could not read progress file, starting from scratch: {e}")

    def write_progress(fi, oi):
        try:
            with open(progress_file, "w", encoding="utf-8") as pfw:
                json.dump({"fileIndex": fi, "orderIndex": oi}, pfw)
        except Exception as e:
            print(f"Warning: could not write progress file: {e}")

    current_file = -1
    current_order = -1
    for fileIndex, orderIndex, order, fp in loadOrdersJsonFiles_indexed(jsonDir):
        # skip until resume point
        if fileIndex < start_file_index:
            continue
        if fileIndex == start_file_index and orderIndex < start_order_index:
            continue

        current_file = fileIndex
        current_order = orderIndex
        fileCount += 1

        docs = buildOrderItemDocsFromOrder(order, db, allowMissingOrder=allowMissing)
        if not docs:
            skippedOrders += 1
            # update progress for skipped order (we processed it)
            write_progress(fileIndex, orderIndex + 1)
            continue

        for d in docs:
            buffer.append(d)
            if len(buffer) >= batchSize:
                try:
                    res = db.orderItems.insert_many(buffer, ordered=False)
                    inserted += len(res.inserted_ids)
                    print(f"Inserted batch (running): {len(res.inserted_ids)} items (total inserted: {inserted})")
                    # persist progress after successful batch
                    write_progress(fileIndex, orderIndex + 1)
                except BulkWriteError as bwe:
                    print(f"BulkWriteError during streaming insert: {getattr(bwe, 'details', bwe)}")
                except Exception as e:
                    print(f"Error during streaming insert: {e}")
                buffer = []

            if maxItems and inserted >= maxItems:
                break

        # after processing an order, persist progress if buffer is empty (i.e., we've flushed recent changes)
        if not buffer:
            write_progress(fileIndex, orderIndex + 1)

        if maxItems and inserted >= maxItems:
            break

    # flush remaining buffer
    if buffer:
        try:
            res = db.orderItems.insert_many(buffer, ordered=False)
            inserted += len(res.inserted_ids)
            print(f"Inserted final batch: {len(res.inserted_ids)} items (total inserted: {inserted})")
        except BulkWriteError as bwe:
            print(f"BulkWriteError on final batch: {getattr(bwe, 'details', bwe)}")
        except Exception as e:
            print(f"Error inserting final batch: {e}")

    print(f"Finished. Inserted (approx) {inserted} documents into 'orderItems' collection; processed {fileCount} files; skipped {skippedOrders} orders")
    closeConnection(mongoClient)


if __name__ == "__main__":
    main()
