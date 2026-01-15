from connection import connectToMongoDB, closeConnection
from helpers import timeAggregation, explainAggregation
from createIndexesOnDocker import createIndexes, createAdditionalIndexes
from bson import json_util
import os
import json


EXPLAIN_FILE = './Embedding/sharding/explainPipelines.json'


def saveExplain(record):
    try:
        if os.path.exists(EXPLAIN_FILE):
            with open(EXPLAIN_FILE, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
        else:
            data = []
    except Exception:
        data = []

    # Ensure explain output is JSON-serializable (convert BSON types to JSON)
    if isinstance(record, dict) and 'explain' in record:
        try:
            # Convert BSON explain to a JSON-compatible Python object
            record['explain'] = json.loads(json_util.dumps(record['explain']))
        except Exception:
            record['explain'] = str(record['explain'])

    data.append(record)

    with open(EXPLAIN_FILE, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)



# Inefficient pipelines

def productsPipelineInefficient():
    # Result: ranked list of top-rated products based on customer reviews.
    pipeline = [
        {"$unwind": {"path": "$reviews", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$_id", "avgRating": {"$avg": "$reviews.rating"}, "name": {"$first": "$name"}, "sku": {"$first": "$sku"}, "reviewsCount": {"$sum": 1}}},
        {"$project": {"name": 1, "sku": 1, "avgRating": 1, "reviewsCount": 1}},
        {"$sort": {"avgRating": -1}},
        {"$match": {"avgRating": {"$gt": 4}}}     # late filter -> forces work on all docs
    ]
    return pipeline



def usersPipelineInefficient():
    # Result: users whose current shopping cart value exceeds 100
    pipeline = [
        {"$unwind": {"path": "$shoppingCart", "preserveNullAndEmptyArrays": True}},
        {"$lookup": {
            "from": "products",
            "localField": "shoppingCart.sku",
            "foreignField": "sku",
            "as": "productInfo"
        }},
        {"$unwind": {"path": "$productInfo", "preserveNullAndEmptyArrays": True}},
        {"$addFields": {"lineTotal": {"$multiply": ["$shoppingCart.quantity", {"$ifNull": ["$productInfo.price", "$shoppingCart.price"]}]}}},
        {"$group": {"_id": "$_id", "username": {"$first": "$username"}, "cartTotal": {"$sum": "$lineTotal"}}},
        {"$project": {"username": 1, "cartTotal": 1}},
        {"$sort": {"cartTotal": -1}},
        {"$match": {"cartTotal": {"$gt": 100}}}   # late match
    ]
    return pipeline


def ordersPipelineInefficient():
    # Returns vendor-level summary documents with fields `totalSales` and
    # `uniqueOrders`. Inefficient variant: unwind items, group by
    # `items.vendor.companyName` and filter late.
    pipeline = [
        {"$unwind": {"path": "$items", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$items.vendor.companyName", "totalSales": {"$sum": {"$multiply": ["$items.unitPrice", "$items.quantity"]}}, "orders": {"$addToSet": "$_id"}}},
        {"$project": {"totalSales": 1, "uniqueOrders": {"$size": {"$ifNull": ["$orders", []]}}}},
        {"$sort": {"totalSales": -1}},
        {"$match": {"totalSales": {"$gt": 1000}}},   # late match
    ]
    return pipeline


# Efficient pipelines

def productsPipelineEfficient():
    # Result: ranked list of top-rated products based on customer reviews.
    pipeline = [
        # 1. PROJECT & CALCULATE (Replaces Unwind + Group)
        # Instead of exploding the data with Unwind, we calculate 
        # the average and count directly within the document.
        # This reduces complexity from O(N*M) to O(N).
        {"$project": {
            "name": 1,
            "sku": 1,
            "avgRating": {"$avg": "$reviews.rating"},
            "reviewsCount": {"$size": {"$ifNull": ["$reviews", []]}}
        }},

        # 2. MATCH (Moved Up)
        # We apply the filter immediately after calculation.
        # Very important to do this before sorting
        {"$match": {
            "avgRating": {"$gt": 4}
        }},

        # 3. SORT
        # Sorting a smaller & filtered dataset
        {"$sort": {
            "avgRating": -1
        }}
    ]
    return pipeline


def usersPipelineEfficient():
    # Result: users whose current shopping cart value exceeds 100
    pipeline = [
        # 1. EARLY FILTER
        # We skip any user who doesn't even have a cart
        {"$match": {"shoppingCart.0": {"$exists": True}}},

        # 2. UNWIND
        # decent - shopping carts are not usually very big
        {"$unwind": "$shoppingCart"},

        # 3. LOOKUP
        {"$lookup": {
            "from": "products",
            "localField": "shoppingCart.sku",
            "foreignField": "sku",
            "as": "productInfo"
        }},

        # 4. FLATTEN LOOKUP
        # We keep "preserveNull" to respect fallback logic later
        {"$unwind": {"path": "$productInfo", "preserveNullAndEmptyArrays": True}},

        # 5. GROUP & CALCULATE (Combined Step)
        # We sum the total directly here
        {"$group": {
            "_id": "$_id",
            "username": {"$first": "$username"},
            "cartTotal": {
                "$sum": {
                    "$multiply": [
                        "$shoppingCart.quantity",
                        # The Fallback Logic: DB Price -> Cart Price
                        {"$ifNull": ["$productInfo.price", "$shoppingCart.price"]}
                    ]
                }
            }
        }},

        # 6. FILTER FINAL RESULTS
        {"$match": {"cartTotal": {"$gt": 100}}},

        # 7. SORT
        {"$sort": {"cartTotal": -1}}
    ]
    return pipeline


def ordersPipelineEfficient():
    # Result: vendors who have generated more than 1000 in revenue
    pipeline = [
        # 1. UNWIND
        # Optimization: Removed "preserveNullAndEmptyArrays"
        {"$unwind": "$items"},

        # 2. GROUP
        # We aggregate the data. We must use $addToSet to handle the 
        # "Unique Orders" logic correctly.
        {"$group": {
            "_id": "$items.vendor.companyName",
            "totalSales": {
                "$sum": {"$multiply": ["$items.unitPrice", "$items.quantity"]}
            },
            # We collect IDs temporarily to count them in the next step
            "orders": {"$addToSet": "$_id"}
        }},

        # 3. MATCH
        # We apply the filter immediately after grouping
        {"$match": {"totalSales": {"$gt": 1000}}},

        # 4. PROJECT
        # Now we calculate the size of the "orders" array.
        # Doing this after the match means we only do it for the "winners".
        {"$project": {
            "totalSales": 1,
            "uniqueOrders": {"$size": "$orders"}
        }},

        # 5. SORT
        # We sort only the filtered list
        {"$sort": {"totalSales": -1}}
    ]
    return pipeline


def dropAllIndexes(db):
    print('\nDropping all non-_id indexes on collections...')
    for name in ['products', 'users', 'orders']:
        coll = db[name]
        try:
            coll.drop_indexes()
            print(f'Dropped indexes on {name}')
        except Exception as e:
            print(f'Error dropping indexes on {name}: {e}')


def runPipelines(db):
    products = db['products']
    users = db['users']
    orders = db['orders']

    print('\n    Running INEFFICIENT pipelines (no indexes)')
    p1 = productsPipelineInefficient()
    results, elapsed = timeAggregation(products, p1, name='Products Inefficient')
    explain = explainAggregation(products, p1)
    saveExplain({
        'stage': 'inefficient_no_indexes',
        'pipeline': p1,
        'name': 'Products Inefficient',
        'elapsedMs': elapsed,
        'resultCount': len(results),
        'explain': explain
    })

    p2 = usersPipelineInefficient()
    results, elapsed = timeAggregation(users, p2, name='Users Inefficient')
    explain = explainAggregation(users, p2)
    saveExplain({
        'stage': 'inefficient_no_indexes',
        'pipeline': p2,
        'name': 'Users Inefficient',
        'elapsedMs': elapsed,
        'resultCount': len(results),
        'explain': explain
    })

    p3 = ordersPipelineInefficient()
    results, elapsed = timeAggregation(orders, p3, name='Orders Inefficient')
    explain = explainAggregation(orders, p3)
    saveExplain({
        'stage': 'inefficient_no_indexes',
        'pipeline': p3,
        'name': 'Orders Inefficient',
        'elapsedMs': elapsed,
        'resultCount': len(results),
        'explain': explain
    })


def runPipelinesWithIndexes(db):
    products = db['products']
    users = db['users']
    orders = db['orders']

    print('\n    Running INEFFICIENT pipelines (with indexes created)')
    p1 = productsPipelineInefficient()
    results, elapsed = timeAggregation(products, p1, name='Products Inefficient with Indexes')
    explain = explainAggregation(products, p1)
    saveExplain({
        'stage': 'inefficient_with_indexes',
        'pipeline': p1,
        'name': 'Products Inefficient with Indexes',
        'elapsedMs': elapsed,
        'resultCount': len(results),
        'explain': explain
    })

    p2 = usersPipelineInefficient()
    results, elapsed = timeAggregation(users, p2, name='Users Inefficient with Indexes')
    explain = explainAggregation(users, p2)
    saveExplain({
        'stage': 'inefficient_with_indexes',
        'pipeline': p2,
        'name': 'Users Inefficient with Indexes',
        'elapsedMs': elapsed,
        'resultCount': len(results),
        'explain': explain
    })

    p3 = ordersPipelineInefficient()
    results, elapsed = timeAggregation(orders, p3, name='Orders Inefficient with Indexes')
    explain = explainAggregation(orders, p3)
    saveExplain({
        'stage': 'inefficient_with_indexes',
        'pipeline': p3,
        'name': 'Orders Inefficient with Indexes',
        'elapsedMs': elapsed,
        'resultCount': len(results),
        'explain': explain
    })


def runOptimizedPipelines(db):
    products = db['products']
    users = db['users']
    orders = db['orders']

    print('\n    Running OPTIMIZED pipelines (with indexes)')
    p1 = productsPipelineEfficient()
    results, elapsed = timeAggregation(products, p1, name='Products Efficient')
    explain = explainAggregation(products, p1)
    saveExplain({
        'stage': 'optimized_with_indexes',
        'pipeline': p1,
        'name': 'Products Efficient',
        'elapsedMs': elapsed,
        'resultCount': len(results),
        'explain': explain
    })

    p2 = usersPipelineEfficient()
    results, elapsed = timeAggregation(users, p2, name='Users Efficient')
    explain = explainAggregation(users, p2)
    saveExplain({
        'stage': 'optimized_with_indexes',
        'pipeline': p2,
        'name': 'Users Efficient',
        'elapsedMs': elapsed,
        'resultCount': len(results),
        'explain': explain
    })

    p3 = ordersPipelineEfficient()
    results, elapsed = timeAggregation(orders, p3, name='Orders Efficient')
    explain = explainAggregation(orders, p3)
    saveExplain({
        'stage': 'optimized_with_indexes',
        'pipeline': p3,
        'name': 'Orders Efficient',
        'elapsedMs': elapsed,
        'resultCount': len(results),
        'explain': explain
    })


def runOptimizedPipelinesAdditional(db):
    products = db['products']
    users = db['users']
    orders = db['orders']

    print('\n    Running OPTIMIZED pipelines (with ADDITIONAL indexes)')
    p1 = productsPipelineEfficient()
    results, elapsed = timeAggregation(products, p1, name='Products Efficient')
    explain = explainAggregation(products, p1)
    saveExplain({
        'stage': 'optimized_with_additional_indexes',
        'pipeline': p1,
        'name': 'Products Efficient',
        'elapsedMs': elapsed,
        'resultCount': len(results),
        'explain': explain
    })

    p2 = usersPipelineEfficient()
    results, elapsed = timeAggregation(users, p2, name='Users Efficient')
    explain = explainAggregation(users, p2)
    saveExplain({
        'stage': 'optimized_with_additional_indexes',
        'pipeline': p2,
        'name': 'Users Efficient',
        'elapsedMs': elapsed,
        'resultCount': len(results),
        'explain': explain
    })

    p3 = ordersPipelineEfficient()
    results, elapsed = timeAggregation(orders, p3, name='Orders Efficient')
    explain = explainAggregation(orders, p3)
    saveExplain({
        'stage': 'optimized_with_additional_indexes',
        'pipeline': p3,
        'name': 'Orders Efficient',
        'elapsedMs': elapsed,
        'resultCount': len(results),
        'explain': explain
    })



def main():
    client, db = connectToMongoDB()

    try:
        # 1. Drop all indexes
        dropAllIndexes(db)

        # 2. Run inefficient pipelines (no indexes)
        runPipelines(db)

        # 3. Create indexes
        createIndexes(db)

        # 4. Run inefficient pipelines again (with indexes present)
        runPipelinesWithIndexes(db)

        # 5. Run optimized pipelines with the query indexes
        runOptimizedPipelines(db)

        # 5. Run optimized pipelines with additional indexes
        createAdditionalIndexes(db)
        
        runOptimizedPipelinesAdditional(db)

    finally:
        closeConnection(client)


if __name__ == '__main__':
    main()
