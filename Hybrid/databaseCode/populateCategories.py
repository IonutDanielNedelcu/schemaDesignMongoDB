import json
from pathlib import Path
from collections import OrderedDict
from bson import ObjectId
from connection import connectToMongoDB, closeConnection
import os


def extractCategories(productsDir):
    mainSet = OrderedDict()
    subSet = OrderedDict()

    for p in sorted(productsDir.glob('*.json')):
        try:
            text = p.read_text(encoding='utf-8')
            data = json.loads(text)
        except Exception:
            # try JSON Lines
            data = []
            try:
                for line in p.read_text(encoding='utf-8').splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        data.append(obj)
                    except Exception:
                        continue
            except Exception:
                continue

        if not isinstance(data, list):
            continue

        for prod in data:
            cat = prod.get('category') or {}
            main = cat.get('main') if isinstance(cat, dict) else None
            sub = cat.get('sub') if isinstance(cat, dict) else None
            if main:
                key = main.strip()
                if key and key not in mainSet:
                    mainSet[key] = None
            if sub and main:
                subkey = sub.strip()
                if subkey:
                    # use tuple (main, sub) to keep relation
                    k = (main.strip(), subkey)
                    if k not in subSet:
                        subSet[k] = None

    # Assign ObjectIds
    for name in list(mainSet.keys()):
        mainSet[name] = ObjectId()

    for (main, sub) in list(subSet.keys()):
        parentId = mainSet.get(main)
        subSet[(main, sub)] = ObjectId()

    # Build output list: main categories first, then subcategories
    out = []
    for name, oid in mainSet.items():
        out.append({
            "_id": str(oid),
            "name": name,
            "parentCategoryId": None
        })

    for (main, sub), oid in subSet.items():
        out.append({
            "_id": str(oid),
            "name": sub,
            "parentCategoryId": str(mainSet.get(main)) if main in mainSet else None
        })

    return out


def insertToMongo(outList):
    # Insert into the Hybrid database using local connection helper
    try:
        
        client, db = connectToMongoDB(dbName="eCommerceProjectHybrid")
        if db is None:
            print('Could not obtain Hybrid database connection; skipping DB insert')
            return

        coll = db.get_collection('categories')
        docs = []
        from bson import ObjectId as BObjectId
        for d in outList:
            doc = d.copy()
            doc['_id'] = BObjectId(doc['_id'])
            if doc['parentCategoryId'] is not None:
                doc['parentCategoryId'] = BObjectId(doc['parentCategoryId'])
            docs.append(doc)

        coll.insert_many(docs, ordered=False)
        print(f"Inserted {len(docs)} documents into {db.name}.categories")
    except Exception as e:
        print('DB insert failed:', e)
    finally:
        try:
            if 'client' in locals() and client:
                closeConnection(client)
        except Exception:
            try:
                client.close()
            except Exception:
                pass


if __name__ == '__main__':
    base = Path(__file__).parent
    productsDir = base / 'JsonProducts'
    if not productsDir.exists():
        print('JsonProducts folder not found at', productsDir)
        raise SystemExit(1)

    out = extractCategories(productsDir)

    # optional DB insert
    insertToMongo(out)
