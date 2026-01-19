from connection import connectToMongoDB, closeConnection
from helpers import timeAggregation, explainAggregation
from indexes import createIndexes
from bson import json_util
import os
import json


EXPLAIN_FILE = './Referencing/queries&strategy/explainPipelines.json'


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
    # Result: ranked list of top-rated products based on customer reviews
    # This pipeline performs a lookup from `reviews` and aggregates ratings
    pipeline = [
        {"$lookup": {"from": "reviews", "localField": "_id", "foreignField": "productId", "as": "reviewsDocs"}},
        {"$unwind": {"path": "$reviewsDocs", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$_id", "avgRating": {"$avg": "$reviewsDocs.rating"}, "name": {"$first": "$name"}, "sku": {"$first": "$sku"}, "reviewsCount": {"$sum": {"$cond": [{"$ifNull": ["$reviewsDocs._id", False]}, 1, 0]}}}},
        {"$project": {"name": 1, "sku": 1, "avgRating": 1, "reviewsCount": 1}},
        {"$sort": {"avgRating": -1}},
        {"$match": {"avgRating": {"$gt": 4}}}
    ]
    return pipeline



def usersPipelineInefficient():
    # Result: users whose current shopping cart value exceeds 100
    pipeline = [
        # shoppingCart holds ObjectId references to shoppingCartItems
        {"$unwind": {"path": "$shoppingCart", "preserveNullAndEmptyArrays": True}},
        {"$lookup": {
            "from": "shoppingCartItems",
            "localField": "shoppingCart",
            "foreignField": "_id",
            "as": "cartItem"
        }},
        {"$unwind": {"path": "$cartItem", "preserveNullAndEmptyArrays": True}},
        {"$lookup": {
            "from": "products",
            "localField": "cartItem.productId",
            "foreignField": "_id",
            "as": "productInfo"
        }},
        {"$unwind": {"path": "$productInfo", "preserveNullAndEmptyArrays": True}},
        {"$addFields": {"lineTotal": {"$multiply": ["$cartItem.quantity", {"$ifNull": ["$productInfo.price", "$cartItem.price"]}]}}},
        {"$group": {"_id": "$_id", "username": {"$first": "$username"}, "cartTotal": {"$sum": "$lineTotal"}}},
        {"$project": {"username": 1, "cartTotal": 1}},
        {"$sort": {"cartTotal": -1}},
        {"$match": {"cartTotal": {"$gt": 100}}}   # late match
    ]
    return pipeline


def ordersPipelineInefficient():
    # Returns vendor-level summary documents with fields `totalSales` and
    # `uniqueOrders`. Inefficient variant: unwind items, group by
    # `items.vendor.companyName` and filter late
    # This pipeline aggregates over `orderItems` (expecting fields: orderId, unitPriceSnapshot, quantity)
    # We need to lookup product price, compute line totals, then group by vendorId
    pipeline = [
        {"$lookup": {"from": "products", "localField": "productId", "foreignField": "_id", "as": "product"}},
        {"$unwind": {"path": "$product", "preserveNullAndEmptyArrays": True}},
        {"$addFields": {"lineTotal": {"$multiply": [{"$ifNull": ["$quantity", 0]}, {"$ifNull": ["$product.price", 0]}]}}},
        {"$group": {"_id": "$vendorId", "totalSales": {"$sum": "$lineTotal"}, "orders": {"$addToSet": "$orderId"}}},
        {"$lookup": {"from": "vendors", "localField": "_id", "foreignField": "_id", "as": "vendorInfo"}},
        {"$unwind": {"path": "$vendorInfo", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "vendorId": "$_id",
            "companyName": {"$ifNull": ["$vendorInfo.companyName", "(unknown)"]},
            "contactEmail": {"$ifNull": ["$vendorInfo.contactEmail", None]},
            "supportPhone": {"$ifNull": ["$vendorInfo.supportPhone", None]},
            "totalSales": 1,
            "uniqueOrders": {"$size": {"$ifNull": ["$orders", []]}}
        }},
        {"$sort": {"totalSales": -1}},
        {"$match": {"totalSales": {"$gt": 1000}}},
    ]
    return pipeline


# Efficient pipelines
def productsPipelineEfficient():
    # Result: ranked list of top-rated products based on customer reviews
    # Efficient variant: lookup reviews once and compute aggregates per product
    pipeline = [
        {"$lookup": {"from": "reviews", "localField": "_id", "foreignField": "productId", "as": "reviewsDocs"}},
        {"$addFields": {"avgRating": {"$cond": [{"$gt": [{"$size": "$reviewsDocs"}, 0]}, {"$avg": "$reviewsDocs.rating"}, None]}, "reviewsCount": {"$size": "$reviewsDocs"}}},
        {"$match": {"avgRating": {"$gt": 4}}},
        {"$project": {"name": 1, "sku": 1, "avgRating": 1, "reviewsCount": 1}},
        {"$sort": {"avgRating": -1}}
    ]
    return pipeline


def usersPipelineEfficient():
    # Result: users whose current shopping cart value exceeds 100
    pipeline = [
        # 1. EARLY FILTER
        # We skip any user who doesn't even have a cart
        {"$match": {"shoppingCart.0": {"$exists": True}}},

        # 2. UNWIND shoppingCart references
        {"$unwind": "$shoppingCart"},

        # 3. LOOKUP shoppingCartItems by id
        {"$lookup": {
            "from": "shoppingCartItems",
            "localField": "shoppingCart",
            "foreignField": "_id",
            "as": "cartItem"
        }},

        # 4. FLATTEN LOOKUP
        {"$unwind": {"path": "$cartItem", "preserveNullAndEmptyArrays": True}},

        # 5. LOOKUP product info
        {"$lookup": {
            "from": "products",
            "localField": "cartItem.productId",
            "foreignField": "_id",
            "as": "productInfo"
        }},

        {"$unwind": {"path": "$productInfo", "preserveNullAndEmptyArrays": True}},

        # 6. GROUP & CALCULATE (Combined Step)
        {"$group": {
            "_id": "$_id",
            "username": {"$first": "$username"},
            "cartTotal": {
                "$sum": {
                    "$multiply": [
                        "$cartItem.quantity",
                        {"$ifNull": ["$productInfo.price", "$cartItem.price"]}
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
        {"$lookup": {"from": "products", "localField": "productId", "foreignField": "_id", "as": "product"}},
        {"$unwind": {"path": "$product", "preserveNullAndEmptyArrays": True}},
        {"$addFields": {"lineTotal": {"$multiply": [{"$ifNull": ["$quantity", 0]}, {"$ifNull": ["$product.price", 0]}]}}},
        {"$group": {"_id": "$vendorId", "totalSales": {"$sum": "$lineTotal"}, "orders": {"$addToSet": "$orderId"}}},
        {"$match": {"totalSales": {"$gt": 1000}}},
        {"$lookup": {"from": "vendors", "localField": "_id", "foreignField": "_id", "as": "vendorInfo"}},
        {"$unwind": {"path": "$vendorInfo", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "vendorId": "$_id",
            "companyName": {"$ifNull": ["$vendorInfo.companyName", "(unknown)"]},
            "contactEmail": {"$ifNull": ["$vendorInfo.contactEmail", None]},
            "supportPhone": {"$ifNull": ["$vendorInfo.supportPhone", None]},
            "totalSales": 1,
            "uniqueOrders": {"$size": {"$ifNull": ["$orders", []]}}
        }},
        {"$sort": {"totalSales": -1}}
    ]
    return pipeline


def dropAllIndexes(db):
    print('\nDropping all non-_id indexes on collections...')
    for name in ['products', 'users', 'orders', 'categories', 'addresses', 'orderItems', 'shoppingCartItems']:
        coll = db[name]
        try:
            coll.drop_indexes()
            print(f'Dropped indexes on {name}')
        except Exception as e:
            print(f'Error dropping indexes on {name}: {e}')


def runPipelines(db):
    products = db['products']
    users = db['users']
    orderItems = db['orderItems']

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
    results, elapsed = timeAggregation(orderItems, p3, name='OrderItems Inefficient')
    explain = explainAggregation(orderItems, p3)
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
    orderItems = db['orderItems']

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
    results, elapsed = timeAggregation(orderItems, p3, name='OrderItems Inefficient with Indexes')
    explain = explainAggregation(orderItems, p3)
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
    orderItems = db['orderItems']

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
    results, elapsed = timeAggregation(orderItems, p3, name='OrderItems Efficient')
    explain = explainAggregation(orderItems, p3)
    saveExplain({
        'stage': 'optimized_with_indexes',
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

    finally:
        closeConnection(client)


if __name__ == '__main__':
    main()
