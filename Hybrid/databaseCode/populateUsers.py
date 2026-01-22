import json
import os
from pathlib import Path
from bson import ObjectId
from connection import connectToMongoDB, closeConnection


def buildProductMap(jsonProductsDir):
    productMap = {}
    if not jsonProductsDir.exists():
        return productMap

    for p in sorted(jsonProductsDir.glob('*.json')):
        try:
            text = p.read_text(encoding='utf-8')
            data = json.loads(text)
        except Exception:
            continue

        if isinstance(data, list):
            docs = data
        elif isinstance(data, dict):
            docs = [data]
        else:
            docs = []

        for d in docs:
            sku = d.get('sku')
            pid = d.get('_id')
            if sku and pid:
                productMap[sku] = pid

    return productMap


def loadUserDocs(jsonUsersDir):
    docs = []
    if not jsonUsersDir.exists():
        return docs

    for p in sorted(jsonUsersDir.glob('*.json')):
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
    # recursively walk obj and convert keys that end with 'sku' or equal 'sku'
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


def normalizeProductId(pid):
    
    try:
        if isinstance(pid, dict) and '$oid' in pid:
            return ObjectId(pid['$oid'])
        if isinstance(pid, str) and len(pid) == 24:
            return ObjectId(pid)
        if isinstance(pid, ObjectId):
            return pid
    except Exception:
        pass
    return None


def normalizeShoppingCart(cart, productMap):
    # transform entries to {productId: ObjectId, quantity: Number}
    if not isinstance(cart, list):
        return
    newCart = []
    for item in cart:
        if not isinstance(item, dict):
            continue
        # prefer existing productId
        pid = item.get('productId') or None
        if not pid and 'sku' in item:
            pid = productMap.get(item.get('sku'))
        pidObj = normalizeProductId(pid)
        # try sku string if still not found
        if not pidObj and 'sku' in item:
            pidObj = normalizeProductId(productMap.get(item.get('sku')))
        if not pidObj:
            # cannot resolve productId, skip this cart item
            continue
        quantity = item.get('quantity') or item.get('qty') or 1
        try:
            quantity = int(quantity)
        except Exception:
            try:
                quantity = int(float(quantity))
            except Exception:
                quantity = 1
        newCart.append({'productId': pidObj, 'quantity': quantity})
    # replace cart contents
    cart.clear()
    cart.extend(newCart)


def normalizeUserDoc(doc):
    
    if isinstance(doc, dict):
        addresses = doc.get('addresses')
        if isinstance(addresses, list):
            for addr in addresses:
                # ensure expected keys exist; skip deep validation
                if isinstance(addr, dict):
                    # rename postalCode -> zipcode if present
                    if 'postalCode' in addr and 'zipcode' not in addr:
                        addr['zipcode'] = addr.pop('postalCode')

        
        if '_id' in doc:
            try:
                pid = doc.get('_id')
                if isinstance(pid, dict) and '$oid' in pid:
                    doc['_id'] = ObjectId(pid['$oid'])
                elif isinstance(pid, str) and len(pid) == 24:
                    doc['_id'] = ObjectId(pid)
            except Exception:
                pass


def populateUsers():
    repoRoot = Path(__file__).parent
    jsonUsersDir = repoRoot / 'JsonUsers'
    jsonProductsDir = repoRoot / 'JsonProducts'

    print('Building product map from JsonProducts...')
    productMap = buildProductMap(jsonProductsDir)
    print(f'Found {len(productMap)} products')

    print('Loading user documents from JsonUsers...')
    userDocs = loadUserDocs(jsonUsersDir)
    print(f'Loaded {len(userDocs)} user docs')

    if not userDocs:
        print('No user documents found. Exiting.')
        return

    client, db = connectToMongoDB('eCommerceProjectHybrid')
    if db is None:
        print('Database connection failed. Exiting.')
        return

    coll = db.get_collection('users')

    # prefer product map from DB (sku -> ObjectId), fallback to JSON map
    try:
        dbProductMap = {}
        for p in db['products'].find({}, {'sku': 1}):
            sku = p.get('sku')
            pid = p.get('_id')
            if sku and pid:
                dbProductMap[sku] = pid
        if dbProductMap:
            # prefer db IDs; overwrite productMap entries
            for k, v in dbProductMap.items():
                productMap[k] = v
            print(f'Loaded {len(dbProductMap)} products from DB for sku->id mapping')
    except Exception:
        pass

    # transform user docs: replace/augment sku references with productIds
    for doc in userDocs:
        transformSkusToProductIds(doc, productMap)
        normalizeUserDoc(doc)
        # normalize shoppingCart to {productId:ObjectId, quantity:Number}
        normalizeShoppingCart(doc.get('shoppingCart'), productMap)


    # insert in batches
    batchSize = 500
    inserted = 0
    try:
        for i in range(0, len(userDocs), batchSize):
            batch = userDocs[i:i+batchSize]
            res = coll.insert_many(batch)
            inserted += len(res.inserted_ids)
            print(f'Inserted batch {i}-{i+len(batch)-1}, {len(res.inserted_ids)} docs')

        print(f'Total inserted documents: {inserted}')

    except Exception as e:
        print(f'Error inserting documents: {e}')

    finally:
        closeConnection(client)


if __name__ == '__main__':
    populateUsers()
