from connection import connectToMongoDB, closeConnection
from helpers import timeAggregation
from queriesIndexes import createIndexes
import os
import json


EXPLAIN_FILE = './Embedding/queries&strategy/explainPipelines.json'


def saveExplain(record):
    try:
        if os.path.exists(EXPLAIN_FILE):
            with open(EXPLAIN_FILE, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
        else:
            data = []
    except Exception:
        data = []

    data.append(record)

    with open(EXPLAIN_FILE, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


def productsPipelineInefficient():
    # Inefficient: unwind reviews, group, then filter (match after grouping -> full scan)
    pipeline = [
        {"$unwind": {"path": "$reviews", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$_id", "avgRating": {"$avg": "$reviews.rating"}, "name": {"$first": "$name"}, "sku": {"$first": "$sku"}}},
        {"$match": {"avgRating": {"$gt": 4}}},
        {"$project": {"name": 1, "sku": 1, "avgRating": 1}}
    ]
    return pipeline


def usersPipelineInefficient():
    # Inefficient: lookup products for each shoppingCart item, then compute cart total, match late
    pipeline = [
        {"$unwind": {"path": "$shoppingCart", "preserveNullAndEmptyArrays": True}},
        {"$lookup": {
            "from": "products",
            "localField": "shoppingCart.sku",
            "foreignField": "sku",
            "as": "productInfo"
        }},
        {"$unwind": {"path": "$productInfo", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$_id", "username": {"$first": "$username"}, "cartTotal": {"$sum": {"$multiply": ["$shoppingCart.quantity", {"$ifNull": ["$productInfo.price", 0]}]}}}},
        # match late (inefficient)
        {"$match": {"cartTotal": {"$gt": 100}}},
        {"$project": {"username": 1, "cartTotal": 1}}
    ]
    return pipeline


def ordersPipelineInefficient():
    # Inefficient: do heavy group across all orders, then filter by date (match after grouping)
    pipeline = [
        {"$unwind": {"path": "$items", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$items.vendor.companyName", "sales": {"$sum": {"$multiply": ["$items.unitPrice", "$items.quantity"]}}}},
        # match late on sales
        {"$match": {"sales": {"$gt": 1000}}},
        {"$sort": {"sales": -1}}
    ]
    return pipeline


def productsPipelineEfficient():
    # Efficient: match category early (uses index on category.main/sub), then compute avg rating
    pipeline = [
        {"$match": {"category.main": "Electronics"}},
        {"$unwind": {"path": "$reviews", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$_id", "avgRating": {"$avg": "$reviews.rating"}, "name": {"$first": "$name"}, "sku": {"$first": "$sku"}}},
        {"$match": {"avgRating": {"$gt": 4}}},
        {"$project": {"name": 1, "sku": 1, "avgRating": 1}}
    ]
    return pipeline


def usersPipelineEfficient():
    # Efficient: match on addresses.zipcode early (uses multikey index), then compute cart totals
    pipeline = [
        {"$match": {"addresses.zipcode": "LA3 6JG"}},
        {"$unwind": {"path": "$shoppingCart", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$_id", "username": {"$first": "$username"}, "cartTotal": {"$sum": {"$multiply": ["$shoppingCart.quantity", "$shoppingCart.price"]}}}},
        {"$match": {"cartTotal": {"$gt": 100}}},
        {"$project": {"username": 1, "cartTotal": 1}}
    ]
    return pipeline


def ordersPipelineEfficient():
    # Efficient: match recent dates or status early (uses orderDate and status indexes), then unwind and group
    pipeline = [
        {"$match": {"status": "Pending"}},
        {"$unwind": {"path": "$items", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$items.sku", "quantitySold": {"$sum": "$items.quantity"}, "totalSales": {"$sum": {"$multiply": ["$items.unitPrice", "$items.quantity"]}}}},
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
    saveExplain({
        'stage': 'inefficient_no_indexes',
        'pipeline': p1,
        'name': 'Products Inefficient',
        'elapsedMs': elapsed,
        'resultCount': len(results)
    })

    p2 = usersPipelineInefficient()
    results, elapsed = timeAggregation(users, p2, name='Users Inefficient')
    saveExplain({
        'stage': 'inefficient_no_indexes',
        'pipeline': p2,
        'name': 'Users Inefficient',
        'elapsedMs': elapsed,
        'resultCount': len(results)
    })

    p3 = ordersPipelineInefficient()
    results, elapsed = timeAggregation(orders, p3, name='Orders Inefficient')
    saveExplain({
        'stage': 'inefficient_no_indexes',
        'pipeline': p3,
        'name': 'Orders Inefficient',
        'elapsedMs': elapsed,
        'resultCount': len(results)
    })


def runPipelinesWithIndexes(db):
    products = db['products']
    users = db['users']
    orders = db['orders']

    print('\n    Running INEFFICIENT pipelines (with indexes created)')
    p1 = productsPipelineInefficient()
    results, elapsed = timeAggregation(products, p1, name='Products Inefficient with Indexes')
    saveExplain({
        'stage': 'inefficient_with_indexes',
        'pipeline': p1,
        'name': 'Products Inefficient with Indexes',
        'elapsedMs': elapsed,
        'resultCount': len(results)
    })

    p2 = usersPipelineInefficient()
    results, elapsed = timeAggregation(users, p2, name='Users Inefficient with Indexes')
    saveExplain({
        'stage': 'inefficient_with_indexes',
        'pipeline': p2,
        'name': 'Users Inefficient with Indexes',
        'elapsedMs': elapsed,
        'resultCount': len(results)
    })

    p3 = ordersPipelineInefficient()
    results, elapsed = timeAggregation(orders, p3, name='Orders Inefficient with Indexes')
    saveExplain({
        'stage': 'inefficient_with_indexes',
        'pipeline': p3,
        'name': 'Orders Inefficient with Indexes',
        'elapsedMs': elapsed,
        'resultCount': len(results)
    })


def runOptimizedPipelines(db):
    products = db['products']
    users = db['users']
    orders = db['orders']

    print('\n    Running OPTIMIZED pipelines (with indexes)')
    p1 = productsPipelineEfficient()
    results, elapsed = timeAggregation(products, p1, name='Products Efficient')
    saveExplain({
        'stage': 'optimized_with_indexes',
        'pipeline': p1,
        'name': 'Products Efficient',
        'elapsedMs': elapsed,
        'resultCount': len(results)
    })

    p2 = usersPipelineEfficient()
    results, elapsed = timeAggregation(users, p2, name='Users Efficient')
    saveExplain({
        'stage': 'optimized_with_indexes',
        'pipeline': p2,
        'name': 'Users Efficient',
        'elapsedMs': elapsed,
        'resultCount': len(results)
    })

    p3 = ordersPipelineEfficient()
    results, elapsed = timeAggregation(orders, p3, name='Orders Efficient')
    saveExplain({
        'stage': 'optimized_with_indexes',
        'pipeline': p3,
        'name': 'Orders Efficient',
        'elapsedMs': elapsed,
        'resultCount': len(results)
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

        # 5. Run optimized pipelines (make them efficient and run with indexes)
        runOptimizedPipelines(db)

    finally:
        closeConnection(client)


if __name__ == '__main__':
    main()
