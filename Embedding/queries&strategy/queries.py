from connection import connectToMongoDB, closeConnection
from indexes import (
    productsSkuUnique,
    productsCategoryCompound,
    productsText,
    createIndexes,
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
import re



def runWithoutIndex(db, collectionName, queryFilter, projection=None, sort=None, limit=None):
    # Returns a dictionary with count, duration, sample, explain or error
    
    collection = db[collectionName]
    try:
        # hint=[('$natural', 1)] -> try to force coll-scan
        noIndexHint = [('$natural', 1)]
        try:
            results, elapsedMs = timeQuery(collection, queryFilter, name=f"{collectionName} noIndex", limit=limit, projection=projection, sort=sort, hint=noIndexHint)
        except Exception:
            # fallback: retry without hint (useful if hint not allowed for this query)
            try:
                results, elapsedMs = timeQuery(collection, queryFilter, name=f"{collectionName} noIndex", limit=limit, projection=projection, sort=sort, hint=None)
            except Exception as e:
                return {'error': str(e)}

        explain = None
        try:
            explain = explainQuery(collection, queryFilter, projection=projection, sort=sort, hint=noIndexHint)
        except Exception:
            try:
                explain = explainQuery(collection, queryFilter, projection=projection, sort=sort, hint=None)
            except Exception:
                explain = None
        return {'count': len(results), 'durationMs': elapsedMs, 'sample': results[:3], 'explain': explain}
    except Exception as e:
        return {'error': str(e)}


def runWithIndex(db, collectionName, queryFilter, indexName=None, projection=None, sort=None, limit=None):
    # Returns a dictionary with count, duration, sample, index, explain or error
    
    collection = db[collectionName]
    try:
        # sends the index as a hint for the query. Do not detect $text; try with the provided hint and fallback to no hint on error.
        hint = indexName if indexName else None
        try:
            results, elapsedMs = timeQuery(collection, queryFilter, name=f"{collectionName} withIndex", limit=limit, projection=projection, sort=sort, hint=hint)
        except Exception:
            try:
                results, elapsedMs = timeQuery(collection, queryFilter, name=f"{collectionName} withIndex", limit=limit, projection=projection, sort=sort, hint=None)
            except Exception as e:
                return {'error': str(e), 'indexHint': indexName}

        explain = None
        try:
            explain = explainQuery(collection, queryFilter, projection=projection, sort=sort, hint=hint)
        except Exception:
            try:
                explain = explainQuery(collection, queryFilter, projection=projection, sort=sort, hint=None)
            except Exception:
                explain = None
        return {'count': len(results), 'durationMs': elapsedMs, 'sample': results[:3], 'indexHint': indexName, 'explain': explain}
    except Exception as e:
        return {'error': str(e), 'indexHint': indexName}


#       MAIN
if __name__ == "__main__":
    client, db = connectToMongoDB()
    try:
        queriesNoIndex = []
        queriesIndex = []

        # 1. Product by SKU
        q = {'sku': 'ELE-ACC-12550'}
        queriesNoIndex.append(('products', q, productsSkuUnique, {'limit': 1}))
        queriesIndex.append(('products', q, productsSkuUnique, {'limit': 1}))

        # 2. Products by category
        q = {'category.main': 'Electronics', 'category.sub': 'Laptops'}
        queriesNoIndex.append(('products', q, productsCategoryCompound, {'limit': 20}))
        queriesIndex.append(('products', q, productsCategoryCompound, {'limit': 20}))

        # 3. Text search products
        searchString = 'gaming laptop'
        # index version: use $text
        qIndex = {'$text': {'$search': searchString}}
        projection = {'score': {'$meta': 'textScore'}}
        sort = [('score', {'$meta': 'textScore'})]
        queriesIndex.append(('products', qIndex, productsText, {'projection': projection, 'sort': sort, 'limit': 10}))

        # no-index version: fallback to regexp OR over common fields to force COLLSCAN
        words = [w for w in re.split(r"\s+", searchString.strip()) if w]
        pattern = '|'.join(re.escape(w) for w in words) if words else re.escape(searchString)
        qNoIndex = {'$or': [
            {'name': {'$regex': pattern, '$options': 'i'}},
            {'details.description': {'$regex': pattern, '$options': 'i'}}
        ]}
        # For no-index run we cannot request textScore metadata, so omit projection/sort using it
        queriesNoIndex.append(('products', qNoIndex, productsText, {'limit': 10}))

        # 4. Find user by email
        q = {'email': 'dennisparker@gmail.com'}
        queriesNoIndex.append(('users', q, usersEmailUnique, {'limit': 1}))
        queriesIndex.append(('users', q, usersEmailUnique, {'limit': 1}))

        # 5. Users by zipcode
        q = {'addresses.zipcode': 'N9F 2WT'}
        queriesNoIndex.append(('users', q, usersAddressesZipcode, {'limit': 20}))
        queriesIndex.append(('users', q, usersAddressesZipcode, {'limit': 20}))

        # 6. Orders by date range
        start = datetime(2021, 1, 1)
        end = datetime(2021, 12, 31)
        q = {'orderDate': {'$gte': start, '$lte': end}}
        sort = [('orderDate', -1)]
        queriesNoIndex.append(('orders', q, ordersOrderDateIdx, {'sort': sort, 'limit': 50}))
        queriesIndex.append(('orders', q, ordersOrderDateIdx, {'sort': sort, 'limit': 50}))

        # 7. Orders by status
        q = {'status': 'Delivered'}
        queriesNoIndex.append(('orders', q, ordersStatusIdx, {'limit': 50}))
        queriesIndex.append(('orders', q, ordersStatusIdx, {'limit': 50}))

        # 8. Orders by customer email
        q = {'customerSnapshot.email': 'sebastianhawkins@outlook.com'}
        sort = [('orderDate', -1)]
        queriesNoIndex.append(('orders', q, ordersCustomerEmailDate, {'sort': sort, 'limit': 50}))
        queriesIndex.append(('orders', q, ordersCustomerEmailDate, {'sort': sort, 'limit': 50}))

        # 9. Orders containing SKU
        q = {'items.sku': 'HOM-DEC-10967'}
        queriesNoIndex.append(('orders', q, ordersItemsSku, {'limit': 50}))
        queriesIndex.append(('orders', q, ordersItemsSku, {'limit': 50}))

        # 10. Pending orders
        q = {'status': 'Pending'}
        queriesNoIndex.append(('orders', q, ordersPendingPartial, {'limit': 50}))
        queriesIndex.append(('orders', q, ordersPendingPartial, {'limit': 50}))

        explainRecords = [] # saved in a JSON for future analysis

        # Phase 1: drop all non-_id indexes from target collections
        print()
        print("Phase 1: Dropping existing indexes from 'products', 'users', 'orders' (keeps _id index)")
        try:
            db['products'].drop_indexes()
            db['users'].drop_indexes()
            db['orders'].drop_indexes()
            print("Indexes dropped.")
        except Exception as e:
            print(f"Could not drop indexes: {e}")

        # Phase 2: run all queries WITHOUT indexes
        print()
        print("Phase 2: Running queries WITHOUT indexes")
        for idx, (collectionName, qfilter, indexName, opts) in enumerate(queriesNoIndex, start=1):
            print()
            print(f"    Query {idx}: collection={collectionName}, index={indexName}")
            resNoIndex = runWithoutIndex(db, collectionName, qfilter, projection=opts.get('projection'), sort=opts.get('sort'), limit=opts.get('limit'))
            print(f"    Result summary:")
            if resNoIndex.get('error'):
                print(f"        Without index: ERROR: {resNoIndex.get('error')}")
                print()
            if resNoIndex.get('explain'):
                print("    Explain (no index):")
                try:
                    printExplainSummary(resNoIndex.get('explain'))
                except Exception as e:
                    print(f"    Could not print explain summary (noIndex): {e}")
                explainRecords.append({
                    'queryNo': idx,
                    'collection': collectionName,
                    'mode': 'noIndexes',
                    'indexHint': 'none',
                    'query': qfilter,
                    'explain': resNoIndex.get('explain')
                })

        # Phase 3: recreate indexes using createIndexes
        print()
        print("Phase 3: Creating indexes using queriesIndexes.createIndexes")
        try:
            createIndexes(db)
            print("Indexes created.")
        except Exception as e:
            print(f"Could not create indexes: {e}")

        # Phase 4: run all queries WITH indexes
        print()
        print("Phase 4: Running queries WITH indexes")
        for idx, (collectionName, qfilter, indexName, opts) in enumerate(queriesIndex, start=1):
            print()
            print(f"    Query {idx}: collection={collectionName}, index={indexName}")
            resIndex = runWithIndex(db, collectionName, qfilter, indexName=indexName, projection=opts.get('projection'), sort=opts.get('sort'), limit=opts.get('limit'))
            print(f"    Result summary:")
            if resIndex.get('error'):
                print(f"        With index: ERROR: {resIndex.get('error')}")
                print()
            if resIndex.get('explain'):
                print()
                print("    Explain (with index):")
                try:
                    printExplainSummary(resIndex.get('explain'))
                except Exception as e:
                    print(f"    Could not print explain summary (withIndex): {e}")
                explainRecords.append({
                    'queryNo': idx,
                    'collection': collectionName,
                    'mode': 'withIndexes',
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
