import json
import os
from pathlib import Path
from datetime import datetime
from bson import ObjectId
from connection import connectToMongoDB, closeConnection


def buildUserMap():
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
    productsColl = db.get_collection('products')
    usersColl = db.get_collection('users')

    for d in orderDocs:
        transformSkusToProductIds(d, productMap)

    productIds = set()
    userIds = set()
    vendorNames = set()
    for d in orderDocs:
        # collect productIds from items
        itemsData = d.get('items') or []
        if isinstance(itemsData, list):
            for it in itemsData:
                pid = it.get('productId')
                if pid:
                    try:
                        # ensure proper ObjectId string -> ObjectId
                        if isinstance(pid, dict) and '$oid' in pid:
                            productIds.add(ObjectId(pid['$oid']))
                        elif isinstance(pid, str) and len(pid) == 24:
                            productIds.add(ObjectId(pid))
                        else:
                            productIds.add(pid)
                    except Exception:
                        productIds.add(pid)

        # collect referenced users via username or userId
        uname = d.get('username')
        if uname and userMap.get(uname):
            userIds.add(userMap.get(uname))
        maybe = d.get('user_id') or d.get('userId') or d.get('_id')
        if isinstance(maybe, str) and userMap.get(maybe):
            userIds.add(userMap.get(maybe))

        # collect vendor names
        vendorField = d.get('vendor') or d.get('vendorName')
        if isinstance(vendorField, str):
            vendorNames.add(vendorField)
        elif isinstance(vendorField, dict):
            n = vendorField.get('name')
            if n:
                vendorNames.add(n)

    # build product snapshot map — load all products to ensure complete coverage
    productSnapshotMap = {}
    try:
        for p in productsColl.find({}, {'name': 1, 'sku': 1, 'price': 1, 'vendorId': 1}):
            productSnapshotMap[p.get('_id')] = p
    except Exception:
        pass

    # build user snapshot map
    userSnapshotMap = {}
    if userIds:
        try:
            ulist = [u for u in userIds]
            for u in usersColl.find({'_id': {'$in': ulist}}, {'username': 1, 'email': 1}):
                userSnapshotMap[u.get('_id')] = u
        except Exception:
            pass

    # build vendor name->id map
    vendorNameToId = {}
    try:
        for v in vendorsColl.find({}, {'name': 1}):
            if v.get('name'):
                vendorNameToId[v.get('name')] = v.get('_id')
    except Exception:
        pass

    print(f'Prefetched products: {len(productSnapshotMap)}, users: {len(userSnapshotMap)}, vendors: {len(vendorNameToId)}')

    # prepare docs: resolve user snapshots, product snapshots, vendorIds
    for doc in orderDocs:
        # normalize provided _id to ObjectId if present
        try:
            if '_id' in doc:
                pid = doc.get('_id')
                if isinstance(pid, dict) and '$oid' in pid:
                    doc['_id'] = ObjectId(pid['$oid'])
                elif isinstance(pid, str) and len(pid) == 24:
                    doc['_id'] = ObjectId(pid)
        except Exception:
            pass
        # normalize orderDate to datetime if string
        if 'orderDate' in doc and isinstance(doc.get('orderDate'), str):
            od = doc.get('orderDate')
            try:
                doc['orderDate'] = datetime.fromisoformat(od)
            except Exception:
                try:
                    doc['orderDate'] = datetime.strptime(od, '%Y-%m-%dT%H:%M:%S')
                except Exception:
                    pass
        # user snapshot: create `user` object with id/username/email snapshots
        userSnapshot = None
        if 'user' in doc and isinstance(doc.get('user'), dict):
            userSnapshot = doc.get('user')

        if not userSnapshot:
            # try to resolve from username or from top-level userId/user_id
            username = doc.get('username')
            uid = None
            if username and userMap.get(username):
                uid = userMap.get(username)
            else:
                maybe = doc.get('user_id') or doc.get('userId') or doc.get('_id')
                if isinstance(maybe, str) and userMap.get(maybe):
                    uid = userMap.get(maybe)

            if uid:
                # fetch user doc for snapshot fields if available
                u = usersColl.find_one({'_id': uid}, {'username': 1, 'email': 1})
                if u:
                    doc['user'] = {
                        'userIdSnapshot': u.get('_id'),
                        'usernameSnapshot': u.get('username'),
                        'emailSnapshot': u.get('email')
                    }

        # vendor resolution for order-level vendor (use prefetched map)
        if 'vendorId' not in doc or not doc.get('vendorId'):
            vendorField = doc.get('vendor') or doc.get('vendorName')
            if isinstance(vendorField, str):
                vid = vendorNameToId.get(vendorField)
                if vid:
                    doc['vendorId'] = vid
            elif isinstance(vendorField, dict):
                name = vendorField.get('name')
                if name:
                    vid = vendorNameToId.get(name)
                    if vid:
                        doc['vendorId'] = vid

        # product resolution in order lines/items: transform SKUs then enrich items
        transformSkusToProductIds(doc, productMap)
        # enrich items with product snapshots (use prefetched map)
        items = doc.get('items') or []
        if isinstance(items, list):
            for item in items:
                # prefer existing productId set by transformSkusToProductIds
                pid = item.get('productId')
                sku = item.get('sku') or item.get('skuSnapshot')
                if not pid and sku:
                    pid = productMap.get(sku)
                    if pid:
                        item['productId'] = pid

                # productId to normalized key for lookup
                try:
                    if 'productId' in item:
                        pval = item.get('productId')
                        if isinstance(pval, dict) and '$oid' in pval:
                            pkey = ObjectId(pval['$oid'])
                        elif isinstance(pval, str) and len(pval) == 24:
                            pkey = ObjectId(pval)
                        else:
                            pkey = pval
                    else:
                        pkey = None
                except Exception:
                    pkey = item.get('productId')

                if pkey and pkey in productSnapshotMap:
                    p = productSnapshotMap.get(pkey)
                    item['productId'] = p.get('_id')
                    item['productNameSnapshot'] = p.get('name')
                    item['skuSnapshot'] = p.get('sku')
                    if 'unitPriceSnapshot' not in item:
                        item['unitPriceSnapshot'] = item.get('unitPrice') or item.get('price') or p.get('price')
                    try:
                        item['quantity'] = int(item.get('quantity', 1))
                    except Exception:
                        try:
                            item['quantity'] = int(float(item.get('quantity', 1)))
                        except Exception:
                            item['quantity'] = 1
                    item['vendorIdSnapshot'] = p.get('vendorId')

        # compute order total if missing
        try:
            if not doc.get('total'):
                total = 0
                for it in items:
                    qty = it.get('quantity', 0) or 0
                    price = it.get('unitPriceSnapshot') or 0
                    try:
                        total += float(price) * int(qty)
                    except Exception:
                        pass
                doc['total'] = total
        except Exception:
            pass

        # normalize shipping details address keys
        sh = doc.get('shippingDetails')
        if isinstance(sh, dict):
            addr = sh.get('address')
            if isinstance(addr, dict):
                if 'postalCode' in addr and 'zipcode' not in addr:
                    addr['zipcode'] = addr.pop('postalCode')


        if 'customerSnapshot' in doc and not doc.get('user'):
            cs = doc.pop('customerSnapshot')
            if isinstance(cs, dict):
                uid = cs.get('_id')
                try:
                    if isinstance(uid, dict) and '$oid' in uid:
                        uid = ObjectId(uid['$oid'])
                    elif isinstance(uid, str) and len(uid) == 24:
                        uid = ObjectId(uid)
                except Exception:
                    pass
                doc['user'] = {
                    'userIdSnapshot': uid,
                    'usernameSnapshot': cs.get('username') or cs.get('name'),
                    'emailSnapshot': cs.get('email')
                }

        if 'user' in doc and isinstance(doc.get('user'), dict):
            u = doc.get('user')
            # if nested user contains full profile, extract minimal snapshot
            if any(k in u for k in ['_id', 'username', 'email']):
                uid = u.get('_id') or u.get('userId') or u.get('userIdSnapshot')
                try:
                    if isinstance(uid, dict) and '$oid' in uid:
                        uid = ObjectId(uid['$oid'])
                    elif isinstance(uid, str) and len(uid) == 24:
                        uid = ObjectId(uid)
                except Exception:
                    pass
                doc['user'] = {
                    'userIdSnapshot': uid,
                    'usernameSnapshot': u.get('username') or u.get('usernameSnapshot') or u.get('name'),
                    'emailSnapshot': u.get('email') or u.get('emailSnapshot')
                }

        # If shippingDetails missing but customer had addresses, use first address
        if not doc.get('shippingDetails'):
            # try to pull from nested user addresses
            maybeUser = doc.get('user')
            if isinstance(maybeUser, dict):
                # we cannot access addresses because we stored only snapshot; skip
                pass

        # Ensure items match canonical shape and remove legacy vendor/product fields
        normalizedItems = []
        for it in items:
            if not isinstance(it, dict):
                continue
            norm = {}
            # productId (ObjectId)
            pid = it.get('productId') or it.get('product_id')
            try:
                if isinstance(pid, dict) and '$oid' in pid:
                    pid = ObjectId(pid['$oid'])
                elif isinstance(pid, str) and len(pid) == 24:
                    pid = ObjectId(pid)
            except Exception:
                pass
            if pid:
                norm['productId'] = pid

            # snapshots
            pname = it.get('productNameSnapshot') or it.get('productName') or it.get('name')
            if pname:
                norm['productNameSnapshot'] = pname

            sku = it.get('skuSnapshot') or it.get('sku')
            if sku:
                norm['skuSnapshot'] = sku

            # quantity
            try:
                norm['quantity'] = int(it.get('quantity', 1))
            except Exception:
                try:
                    norm['quantity'] = int(float(it.get('quantity', 1)))
                except Exception:
                    norm['quantity'] = 1

            # unitPriceSnapshot
            price = it.get('unitPriceSnapshot') or it.get('unitPrice') or it.get('price')
            try:
                if price is not None:
                    norm['unitPriceSnapshot'] = float(price)
            except Exception:
                pass

            # vendorIdSnapshot: prefer vendorIdSnapshot if present, else vendorId from product snapshot
            v = it.get('vendorIdSnapshot') or it.get('vendorId')
            try:
                if isinstance(v, dict) and '$oid' in v:
                    v = ObjectId(v['$oid'])
                elif isinstance(v, str) and len(v) == 24:
                    v = ObjectId(v)
            except Exception:
                pass
            if not v:
                # try from prefetched product
                pkey = pid
                pv = productSnapshotMap.get(pkey)
                if pv:
                    v = pv.get('vendorId')
            if v:
                norm['vendorIdSnapshot'] = v

            # only include items that have productId or skuSnapshot
            if 'productId' in norm or 'skuSnapshot' in norm:
                normalizedItems.append(norm)

        # replace items with normalized items
        doc['items'] = normalizedItems

        # Final enforcement: ensure top-level keys exist per canonical schema
        if '_id' in doc and isinstance(doc.get('_id'), dict) and '$oid' in doc.get('_id'):
            try:
                doc['_id'] = ObjectId(doc.get('_id')['$oid'])
            except Exception:
                pass

        # if order has no items product snapshots, leave as-is


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
