# Index creation helpers for the Referencing dataset

from connection import connectToMongoDB, closeConnection
from pymongo import ASCENDING, DESCENDING, TEXT
from pymongo.collation import Collation


productsSkuUnique = 'productsSkuUnique'
productsText = 'productsText'
productsMainPartial = 'productsMainPartial'
productsSubPartial = 'productsSubPartial'

usersEmailUnique = 'usersEmailUnique'
usersAddressesZipcode = 'usersAddressesZipcode'

ordersOrderDateIdx = 'ordersOrderDateIdx'
ordersStatusIdx = 'ordersStatusIdx'
ordersCustomerEmailDate = 'ordersCustomerEmailDate'
ordersPendingPartial = 'ordersPendingPartial'
orderItemsProductId = 'orderItemsProductId'


def createIndexes(db):
    products = db['products']
    users = db['users']
    addresses = db['addresses']
    orders = db['orders']
    orderItems = db['orderItems']

    productIndexes = [
        {
            'keys': [('sku', ASCENDING)],
            'options': {'unique': True, 'name': productsSkuUnique},
            'type': 'Single-field & Unique'
        },
        {
            'keys': [('name', TEXT), ('details.description', TEXT)],
            'options': {'name': productsText},
            'type': 'Text'
        },
        {
            'keys': [('mainCategoryId', ASCENDING)],
            'options': {'name': productsMainPartial},
            'type': 'Single-field - main category'
        },
        {
            'keys': [('subCategoryId', ASCENDING)],
            'options': {'name': productsSubPartial, 'partialFilterExpression': {'subCategoryId': {'$type': 'objectId'}}},
            'type': 'Partial - products in sub categories'
        },
    ]

    usersIndexes = [
        {
            'keys': [('email', ASCENDING)],
            'options': {'unique': True, 'name': usersEmailUnique, 'collation': Collation('en', strength=2)},
            'type': 'Unique & Case-insensitive'
        },
    ]

    addressesIndexes = [
        {
            'keys': [('zipCode', ASCENDING)],
            'options': {'name': usersAddressesZipcode}, 
            'type': 'Single-field'
        }
    ]

    ordersIndexes = [
        {
            'keys': [('orderDate', DESCENDING)],
            'options': {'name': ordersOrderDateIdx},
            'type': 'Single-field'
        },
        {
            'keys': [('status', ASCENDING)],
            'options': {'name': ordersStatusIdx},
            'type': 'Single-field'
        },
        {
            'keys': [('userId', ASCENDING), ('orderDate', DESCENDING)],
            'options': {'name': ordersCustomerEmailDate},
            'type': 'Compound (userId + orderDate)'
        },
        {
            'keys': [('status', ASCENDING)],
            'options': {'name': ordersPendingPartial, 'partialFilterExpression': {'status': 'Pending'}},
            'type': 'Partial'
        },
    ]

    orderItemsIndexes = [
        {
            'keys': [('productId', ASCENDING)],
            'options': {'name': orderItemsProductId},
            'type': 'Single-field (productId)'
        },
    ]

    # helper nested function for creating indexes and reporting CLI information
    def createAndReport(collection, indexDef):
        name = indexDef.get('options', {}).get('name')
        createdName = None
        try:
            createdName = collection.create_index(indexDef['keys'], **indexDef.get('options', {}))
            print(f"Index '{createdName}' on '{collection.name}' (type: {indexDef.get('type')}) created successfully.")
        except Exception as e:
            idxName = createdName or name or str(indexDef.get('keys'))
            print(f"Error creating index '{idxName}' on '{collection.name}': {e}")

    # indexes for products
    print()
    print("Started creating indexes for 'products' collection.")
    for idx in productIndexes:
        createAndReport(products, idx)
    print("Finished creating indexes for 'products' collection.")

    # indexes for users
    print()
    print("Started creating indexes for 'users' collection.")
    for idx in usersIndexes:
        createAndReport(users, idx)
    print("Finished creating indexes for 'users' collection.")

    # indexes for addresses
    print()
    print("Started creating indexes for 'addresses' collection.")
    for idx in addressesIndexes:
        createAndReport(addresses, idx)
    print("Finished creating indexes for 'addresses' collection.")

    # indexes for orders
    print()
    print("Started creating indexes for 'orders' collection.")
    for idx in ordersIndexes:
        createAndReport(orders, idx)
    print("Finished creating indexes for 'orders' collection.")

    # indexes for orderItems
    print()
    print("Started creating indexes for 'orderItems' collection.")
    for idx in orderItemsIndexes:
        createAndReport(orderItems, idx)
    print("Finished creating indexes for 'orderItems' collection.")


if __name__ == '__main__':
    client, db = connectToMongoDB()
    try:
        createIndexes(db)
    finally:
        closeConnection(client)
