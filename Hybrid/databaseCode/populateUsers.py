import json
import os
from pathlib import Path
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

            # key is sku-like
            if isinstance(k, str) and k.lower().endswith('sku') and isinstance(v, str):
                # build new key: replace suffix 'Sku' with 'Id' or fallback to 'productId'
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

    # transform user docs: replace/augment sku references with productIds
    for doc in userDocs:
        transformSkusToProductIds(doc, productMap)

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
