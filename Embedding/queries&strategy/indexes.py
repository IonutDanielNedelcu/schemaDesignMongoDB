from connection import connectToMongoDB, closeConnection
from pymongo import ASCENDING, DESCENDING, TEXT, IndexModel
from pymongo.collation import Collation


productsSkuUnique = 'productsSkuUnique'
productsCategoryCompound = 'productsCategoryCompound'
productsText = 'productsText'

usersEmailUnique = 'usersEmailUnique'
usersAddressesZipcode = 'usersAddressesZipcode'

ordersOrderDateIdx = 'ordersOrderDateIdx'
ordersStatusIdx = 'ordersStatusIdx'
ordersCustomerEmailDate = 'ordersCustomerEmailDate'
ordersItemsSku = 'ordersItemsSku'
ordersPendingPartial = 'ordersPendingPartial'

def createIndexes(db):
    products = db['products']
    users = db['users']
    orders = db['orders']
    
    productIndexes = [
        { 
            'keys': [('sku', ASCENDING)], 
            'options': {'unique': True, 'name': productsSkuUnique}, 
            'type': 'Single-field & Unique'
        },
        { 
            'keys': [('category.main', ASCENDING), ('category.sub', ASCENDING)], 
            'options': {'name': productsCategoryCompound}, 
            'type': 'Compound' 
        },
        { 
            'keys': [('name', TEXT), ('details.description', TEXT)], 
            'options': {'name': productsText}, 
            'type': 'Text' 
        },
    ]

    usersIndexes = [
        { 
            'keys': [('email', ASCENDING)], 
            'options': {'unique': True, 'name': usersEmailUnique, 'collation': Collation('en', strength=2)}, 
            'type': 'Unique & Case-insensitive' 
        },
        { 
            'keys': [('addresses.zipcode', ASCENDING)], 
            'options': {'name': usersAddressesZipcode}, 
            'type': 'Multikey (array field)' 
        },
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
            'keys': [('customerSnapshot.email', ASCENDING), ('orderDate', DESCENDING)], 
            'options': {'name': ordersCustomerEmailDate}, 
            'type': 'Compound' 
        },
        { 
            'keys': [('items.sku', ASCENDING)], 
            'options': {'name': ordersItemsSku}, 
            'type': 'Multikey (array field)' 
        },
        { 
            'keys': [('status', ASCENDING)], 
            'options': {'name': ordersPendingPartial, 'partialFilterExpression': {'status': 'Pending'}}, 
            'type': 'Partial' 
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

    # indexes for orders
    print()
    print("Started creating indexes for 'orders' collection.")
    for idx in ordersIndexes:
        createAndReport(orders, idx)
    print("Finished creating indexes for 'orders' collection.")


# if we want it the script to be ran by itself
if __name__ == '__main__':
    client, db = connectToMongoDB()
    try:
        createIndexes(db)
    finally:
        closeConnection(client)


