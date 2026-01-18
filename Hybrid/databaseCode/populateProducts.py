import json
import os
from pathlib import Path
from connection import connectToMongoDB, closeConnection


def buildUserMap(jsonUsersDir):
    userMap = {}
    if not jsonUsersDir.exists():
        return userMap

    for p in sorted(jsonUsersDir.glob('*.json')):
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
            username = d.get('username')
            userId = d.get('_id')
            if username and userId:
                userMap[username] = userId

    return userMap


def loadProductDocs(jsonProductsDir):
    docs = []
    if not jsonProductsDir.exists():
        return docs

    for p in sorted(jsonProductsDir.glob('*.json')):
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


def populateProducts():
    repoRoot = Path(__file__).parent
    jsonUsersDir = repoRoot / 'JsonUsers'
    jsonProductsDir = repoRoot / 'JsonProducts'

    print('Building user map from JsonUsers...')
    userMap = buildUserMap(jsonUsersDir)
    print(f'Found {len(userMap)} users')

    print('Loading product documents from JsonProducts...')
    productDocs = loadProductDocs(jsonProductsDir)
    print(f'Loaded {len(productDocs)} product docs')

    if not productDocs:
        print('No product documents found. Exiting.')
        return

    client, db = connectToMongoDB('eCommerceProjectHybrid')
    if db is None:
        print('Database connection failed. Exiting.')
        return

    coll = db.get_collection('products')

    # prepare docs: attach userId to reviews when possible
    for doc in productDocs:
        reviews = doc.get('reviews')
        if isinstance(reviews, list):
            for rev in reviews:
                if 'userId' not in rev and 'username' in rev:
                    uid = userMap.get(rev.get('username'))
                    if uid:
                        rev['userId'] = uid

    # insert in batches
    batchSize = 500
    inserted = 0
    try:
        for i in range(0, len(productDocs), batchSize):
            batch = productDocs[i:i+batchSize]
            res = coll.insert_many(batch)
            inserted += len(res.inserted_ids)
            print(f'Inserted batch {i}-{i+len(batch)-1}, {len(res.inserted_ids)} docs')

        print(f'Total inserted documents: {inserted}')

    except Exception as e:
        print(f'Error inserting documents: {e}')

    finally:
        closeConnection(client)


if __name__ == '__main__':
    populateProducts()
