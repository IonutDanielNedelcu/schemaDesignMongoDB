import json
import os
from pathlib import Path
from connection import connectToMongoDB, closeConnection


def buildUserMap():
    """Build username -> _id map from DB users collection only."""
    userMap = {}
    client, db = connectToMongoDB('eCommerceProjectHybrid')
    if db is None:
        return userMap

    try:
        for u in db.get_collection('users').find({}, {'username': 1}):
            uname = u.get('username')
            uid = u.get('_id')
            if uname and uid:
                userMap[uname] = uid
            if uid:
                userMap[str(uid)] = uid
    finally:
        closeConnection(client)

    return userMap


def buildProductMap():
    """Build sku -> _id map from DB products collection only."""
    productMap = {}
    client, db = connectToMongoDB('eCommerceProjectHybrid')
    if db is None:
        return productMap

    try:
        for p in db.get_collection('products').find({}, {'sku': 1}):
            sku = p.get('sku')
            pid = p.get('_id')
            if sku and pid:
                productMap[sku] = pid
            if pid:
                productMap[str(pid)] = pid
    finally:
        closeConnection(client)

    return productMap


def loadOrderDocs(jsonOrdersDir):
    docs = []
    if not jsonOrdersDir.exists():
        return docs

    for p in sorted(jsonOrdersDir.glob('*.json')):
        try:
            text = p.read_text(encoding='utf-8')
            data = json.loads(text)
        except Exception:
            print(f'Could not read {p.name}. Skipping.')
            continue

        if isinstance(data, list):
            docs.extend(data)
        elif isinstance(data, dict):
            docs.append(data)

    return docs


def transformSkusToProductIds(obj, productMap):
    if isinstance(obj, dict):
        keys = list(obj.keys())
        for k in keys:
            v = obj[k]
            if isinstance(v, (dict, list)):
                transformSkusToProductIds(v, productMap)

            if isinstance(k, str) and k.lower().endswith('sku') and isinstance(v, str):
                newKey = k[:-3] + 'Id' if len(k) > 3 else 'productId'
                pid = productMap.get(v)
                if pid:
                    obj[newKey] = pid
            elif k == 'sku' and isinstance(v, str):
                pid = productMap.get(v)
                if pid:
                    obj['productId'] = pid

    elif isinstance(obj, list):
        for item in obj:
            transformSkusToProductIds(item, productMap)


def resolveVendorId(order, vendorsColl):
    # If vendorId exists, keep
    if 'vendorId' in order and order.get('vendorId'):
        return order.get('vendorId')

    # vendor field could be string name or dict
    vendorField = order.get('vendor') or order.get('vendorName')
    if isinstance(vendorField, str):
        v = vendorsColl.find_one({'name': vendorField})
        if v:
            return v.get('_id')

    if isinstance(vendorField, dict):
        name = vendorField.get('name')
        if name:
            v = vendorsColl.find_one({'name': name})
            if v:
                return v.get('_id')

    return None


def populateOrders():
    repoRoot = Path(__file__).parent
    jsonUsersDir = repoRoot / 'JsonUsers'
    jsonProductsDir = repoRoot / 'JsonProducts'
    jsonOrdersDir = repoRoot / 'JsonOrders'

    print('Building maps from database users and products...')
    userMap = buildUserMap()
    productMap = buildProductMap()
    print(f'Users: {len(userMap)}, Products: {len(productMap)}')

    print('Loading order documents from JsonOrders...')
    orderDocs = loadOrderDocs(jsonOrdersDir)
    print(f'Loaded {len(orderDocs)} order docs')

    if not orderDocs:
        print('No order documents found. Exiting.')
        return

    client, db = connectToMongoDB('eCommerceProjectHybrid')
    if db is None:
        print('Database connection failed. Exiting.')
        return

    vendorsColl = db.get_collection('vendors')
    ordersColl = db.get_collection('orders')

    # prepare docs: resolve userIds, productIds, vendorIds
    for doc in orderDocs:
        # user resolution
        if 'userId' not in doc:
            # try username or user_id
            username = doc.get('username')
            if username and userMap.get(username):
                doc['userId'] = userMap.get(username)
            else:
                uid = doc.get('user_id') or doc.get('_id')
                if isinstance(uid, str) and userMap.get(uid):
                    doc['userId'] = userMap.get(uid)

        # vendor resolution
        if 'vendorId' not in doc or not doc.get('vendorId'):
            vid = resolveVendorId(doc, vendorsColl)
            if vid:
                doc['vendorId'] = vid

        # product resolution in order lines/items
        transformSkusToProductIds(doc, productMap)

    # insert in batches
    batchSize = 500
    inserted = 0
    try:
        for i in range(0, len(orderDocs), batchSize):
            batch = orderDocs[i:i+batchSize]
            res = ordersColl.insert_many(batch)
            inserted += len(res.inserted_ids)
            print(f'Inserted batch {i}-{i+len(batch)-1}, {len(res.inserted_ids)} docs')

        print(f'Total inserted documents: {inserted}')

    except Exception as e:
        print(f'Error inserting documents: {e}')

    finally:
        closeConnection(client)


if __name__ == '__main__':
    populateOrders()
