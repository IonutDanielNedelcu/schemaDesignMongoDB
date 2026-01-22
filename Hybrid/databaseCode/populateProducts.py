import json
import os
from pathlib import Path
from datetime import datetime
from bson import ObjectId
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
            
            try:
                if isinstance(userId, dict) and '$oid' in userId:
                    userId = ObjectId(userId['$oid'])
                elif isinstance(userId, str) and len(userId) == 24:
                    userId = ObjectId(userId)
            except Exception:
                pass
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
    vendorsColl = db.get_collection('vendors')
    categoriesColl = db.get_collection('categories')

    vendorMap = {}
    try:
        for v in vendorsColl.find({}, {'companyName': 1, 'name': 1}):
            vid = v.get('_id')
            cname = v.get('companyName')
            name = v.get('name')
            if cname:
                vendorMap[cname] = vid
            if name:
                vendorMap[name] = vid
    except Exception:
        vendorMap = {}

    print('Building category maps from DB...')
    mainCategoryMap = {}    # name -> _id for parentCategoryId == None
    subCategoryMap = {}     # (parentId, subName) -> _id
    try:
        for c in categoriesColl.find({}, {'name': 1, 'parentCategoryId': 1}):
            cid = c.get('_id')
            cname = c.get('name')
            parent = c.get('parentCategoryId')
            if parent is None:
                if cname:
                    mainCategoryMap[cname] = cid
            else:
                if cname and parent:
                    subCategoryMap[(parent, cname)] = cid
    except Exception:
        mainCategoryMap = {}
        subCategoryMap = {}
    
    total = len(productDocs)
    for idx, doc in enumerate(productDocs, start=1):
        if idx % 100 == 0:
            print(f'Preparing product {idx}/{total}...')
        
        try:
            if '_id' in doc:
                pid = doc.get('_id')
                if isinstance(pid, dict) and '$oid' in pid:
                    doc['_id'] = ObjectId(pid['$oid'])
                elif isinstance(pid, str) and len(pid) == 24:
                    doc['_id'] = ObjectId(pid)
        except Exception:
            pass
        
        # resolve vendor -> vendorId
        vendorField = doc.get('vendor')
        vendorId = None
        if isinstance(vendorField, dict):
            vname = vendorField.get('companyName') or vendorField.get('name')
            if vname:
                vendorId = vendorMap.get(vname)
        elif isinstance(vendorField, str):
            vendorId = vendorMap.get(vendorField)
        if vendorId:
            doc['vendorId'] = vendorId
            # remove nested vendor object
            if 'vendor' in doc:
                doc.pop('vendor', None)

        # resolve category.main / category.sub -> mainCategoryId / subCategoryId
        cat = doc.get('category')
        if isinstance(cat, dict):
            mainName = cat.get('main')
            subName = cat.get('sub')
            mainId = None
            subId = None
            if mainName:
                mainId = mainCategoryMap.get(mainName)
                if mainId:
                    doc['mainCategoryId'] = mainId
                    # remove nested category object
                    if 'category' in doc:
                        doc.pop('category', None)
                if subName and mainId:
                    subId = subCategoryMap.get((mainId, subName))
                    if subId:
                        doc['subCategoryId'] = subId

        # attach userId to reviews when possible and normalize review fields
        reviews = doc.get('reviews')
        if isinstance(reviews, list):
            for rev in reviews:
                # normalize username field
                username = rev.get('username') or rev.get('userDisplayName') or rev.get('user')
                if username and 'username' not in rev:
                    rev['username'] = username
                
                if 'userId' not in rev and username:
                    uid = userMap.get(username)
                    if uid:
                        rev['userId'] = uid
                else:
                    
                    try:
                        uidval = rev.get('userId')
                        if isinstance(uidval, dict) and '$oid' in uidval:
                            rev['userId'] = ObjectId(uidval['$oid'])
                        elif isinstance(uidval, str) and len(uidval) == 24:
                            rev['userId'] = ObjectId(uidval)
                    except Exception:
                        pass
                
                dateVal = rev.get('date')
                if isinstance(dateVal, str):
                    try:
                        rev['date'] = datetime.fromisoformat(dateVal)
                    except Exception:
                        try:
                            rev['date'] = datetime.strptime(dateVal, '%Y-%m-%dT%H:%M:%S')
                        except Exception:
                            pass
                
                if 'userDisplayName' in rev and 'username' in rev:
                    rev.pop('userDisplayName', None)


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
