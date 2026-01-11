from connection import connectToMongoDB, closeConnection
from queriesIndexes import (
    productsSkuUnique,
    productsCategoryCompound,
    productsText,
    usersEmailUnique,
    usersAddressesZipcode,
    ordersOrderDateIdx,
    ordersStatusIdx,
    ordersCustomerEmailDate,
    ordersItemsSku,
    ordersPendingPartial,
)
from datetime import datetime
from helpers import timeQuery, explainQuery, printExplainSummary
from bson.json_util import dumps


# recursively detects operator '$text'
def containsTextOperator(q):
    if not isinstance(q, dict):
        return False
    for k, v in q.items():
        if k == '$text':
            return True
        if isinstance(v, dict) and containsTextOperator(v):
            return True
        if isinstance(v, list):
            for item in v:
                if isinstance(item, dict) and containsTextOperator(item):
                    return True
    return False

def runWithoutIndex(db, collectionName, queryFilter, projection=None, sort=None, limit=None):
    # Returns a dictionary with count, duration, sample, explain or error
    
    collection = db[collectionName]
    try:
        # hint=[('$natural', 1)] -> forces coll-scan. For text queries MongoDB disallow hint, so omit it.
        noIndexHint = None if containsTextOperator(queryFilter) else [('$natural', 1)]
        results, elapsedMs = timeQuery(collection, queryFilter, name=f"{collectionName} noIndex", limit=limit, projection=projection, sort=sort, hint=noIndexHint)
        explain = None
        try:
            explain = explainQuery(collection, queryFilter, projection=projection, sort=sort, hint=noIndexHint)
        except Exception:
            explain = None
        return {'count': len(results), 'durationMs': elapsedMs, 'sample': results[:3], 'explain': explain}
    except Exception as e:
        return {'error': str(e)}


def runWithIndex(db, collectionName, queryFilter, indexName=None, projection=None, sort=None, limit=None):
    # Returns a dictionary with count, duration, sample, index, explain or error
    
    collection = db[collectionName]
    try:
        # sends the index as a hint for the query. For text queries, omit hint (not allowed).
        hint = None if containsTextOperator(queryFilter) else (indexName if indexName else None)
        results, elapsedMs = timeQuery(collection, queryFilter, name=f"{collectionName} withIndex", limit=limit, projection=projection, sort=sort, hint=hint)
        explain = None
        try:
            explain = explainQuery(collection, queryFilter, projection=projection, sort=sort, hint=hint)
        except Exception:
            explain = None
        return {'count': len(results), 'durationMs': elapsedMs, 'sample': results[:3], 'indexHint': indexName, 'explain': explain}
    except Exception as e:
        return {'error': str(e), 'indexHint': indexName}




#       MAIN
client, db = connectToMongoDB()
try:
    queries = []

    # 1. Product by SKU
    q = {'sku': 'ELE-ACC-12550'}
    queries.append(('products', q, productsSkuUnique, {'limit': 1}))

    # 2. Products by category
    q = {'category.main': 'Electronics', 'category.sub': 'Laptops'}
    queries.append(('products', q, productsCategoryCompound, {'limit': 20}))

    # 3. Text search products
    q = {'$text': {'$search': 'gaming laptop'}}
    projection = {'score': {'$meta': 'textScore'}}
    sort = [('score', {'$meta': 'textScore'})]
    queries.append(('products', q, productsText, {'projection': projection, 'sort': sort, 'limit': 10}))

    # 4. Find user by email
    q = {'email': 'dennisparker@gmail.com'}
    queries.append(('users', q, usersEmailUnique, {'limit': 1}))

    # 5. Users by zipcode
    q = {'addresses.zipcode': 'N9F 2WT'}
    queries.append(('users', q, usersAddressesZipcode, {'limit': 20}))

    # 6. Orders by date range
    start = datetime(2021, 1, 1)
    end = datetime(2021, 12, 31)
    q = {'orderDate': {'$gte': start, '$lte': end}}
    sort = [('orderDate', -1)]
    queries.append(('orders', q, ordersOrderDateIdx, {'sort': sort, 'limit': 50}))

    # 7. Orders by status
    q = {'status': 'Pending'}
    queries.append(('orders', q, ordersStatusIdx, {'limit': 50}))

    # 8. Orders by customer email
    q = {'customerSnapshot.email': 'sebastianhawkins@outlook.com'}
    sort = [('orderDate', -1)]
    queries.append(('orders', q, ordersCustomerEmailDate, {'sort': sort, 'limit': 50}))

    # 9. Orders containing SKU
    q = {'items.sku': 'OFF-ACC-12497'}
    queries.append(('orders', q, ordersItemsSku, {'limit': 50}))

    # 10. Pending orders
    q = {'status': 'Pending'}
    queries.append(('orders', q, ordersPendingPartial, {'limit': 50}))

    explainRecords = [] # saved in a JSON for future analysis
    
    for idx, (collectionName, qfilter, indexName, opts) in enumerate(queries, start=1):
        print()
        print(f"    Query {idx}: collection={collectionName}, index={indexName}")
        resNoIndex = runWithoutIndex(db, collectionName, qfilter, projection=opts.get('projection'), sort=opts.get('sort'), limit=opts.get('limit'))
        resIndex = runWithIndex(db, collectionName, qfilter, indexName=indexName, projection=opts.get('projection'), sort=opts.get('sort'), limit=opts.get('limit'))
        print(f"    Result summary:")
        # concise, always-visible summary (count, duration, sample or error)
        if resNoIndex.get('error'):
            print(f"        Without index: ERROR: {resNoIndex.get('error')}")
            print()
        if resIndex.get('error'):
            print(f"        With index: ERROR: {resIndex.get('error')}")
            print()
        
        # Explain summaries (if available - no errors)
        if resNoIndex.get('explain'):
            print("    Explain (no index):")
            try:
                printExplainSummary(resNoIndex.get('explain'))
            except Exception as e:
                print(f"    Could not print explain summary (noIndex): {e}")
            explainRecords.append({
                'collection': collectionName,
                'mode': 'noIndex',
                'indexHint': indexName,
                'query': qfilter,
                'explain': resNoIndex.get('explain')
            })

        if resIndex.get('explain'):
            print()
            print("    Explain (with index):")
            try:
                printExplainSummary(resIndex.get('explain'))
            except Exception as e:
                print(f"    Could not print explain summary (withIndex): {e}")
            explainRecords.append({
                'collection': collectionName,
                'mode': 'withIndex',
                'indexHint': indexName,
                'query': qfilter,
                'explain': resIndex.get('explain')
            })

    # save explain records to a file (if any)
    try:
        if explainRecords:
            with open('./Embedding/queries&strategy/explainQueries.json', 'w', encoding='utf-8') as f:
                f.write(dumps(explainRecords, indent=2))
            print("Saved explain plans to explainQueries.json")
    except Exception as e:
        print(f"Failed to save explain plans: {e}")
finally:
    closeConnection(client)
