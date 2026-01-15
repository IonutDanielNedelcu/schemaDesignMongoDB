from connection import connectToMongoDB, closeConnection
from pymongo import ASCENDING, DESCENDING, TEXT, HASHED
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

# Additional index names (do not duplicate the ones above)
ordersVendorCompanyIdx = 'ordersVendorCompanyIdx'
ordersCustomerIdDate = 'ordersCustomerIdDate'

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
            'keys': [('_id', HASHED), ('email', ASCENDING)],
            'options': {'name': usersEmailUnique, 'collation': Collation('en', strength=2)},
            'type': 'Unique & Case-insensitive (includes shard key)'
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

    def createAndReport(collection, indexDef):
        name = indexDef.get('options', {}).get('name')
        createdName = None
        try:
            createdName = collection.create_index(indexDef['keys'], **indexDef.get('options', {}))
            print(f"Index '{createdName}' on '{collection.name}' (type: {indexDef.get('type')}) created successfully.")
        except Exception as e:
            idxName = createdName or name or str(indexDef.get('keys'))
            print(f"Error creating index '{idxName}' on '{collection.name}': {e}")

    print()
    print("Started creating indexes for 'products' collection.")
    for idx in productIndexes:
        createAndReport(products, idx)
    print("Finished creating indexes for 'products' collection.")

    print()
    print("Started creating indexes for 'users' collection.")
    for idx in usersIndexes:
        createAndReport(users, idx)
    print("Finished creating indexes for 'users' collection.")

    print()
    print("Started creating indexes for 'orders' collection.")
    for idx in ordersIndexes:
        createAndReport(orders, idx)
    print("Finished creating indexes for 'orders' collection.")


def createAdditionalIndexes(db):
    orders = db['orders']

    ordersAdditionalIndexes = [
        {
            'keys': [('items.vendor.companyName', ASCENDING)],
            'options': {'name': ordersVendorCompanyIdx},
            'type': 'Multikey (items.vendor.companyName)'
        },
        {
            'keys': [('customerSnapshot._id', ASCENDING), ('orderDate', DESCENDING)],
            'options': {'name': ordersCustomerIdDate},
            'type': 'Compound (customer id + date)'
        }
    ]

    # local helper that mirrors createIndexes' reporting behavior
    def createAndReport(collection, indexDef):
        name = indexDef.get('options', {}).get('name')
        try:
            createdName = collection.create_index(indexDef['keys'], **indexDef.get('options', {}))
            print(f"Index '{createdName}' on '{collection.name}' (type: {indexDef.get('type')}) created successfully.")
        except Exception as e:
            idxName = name or str(indexDef.get('keys'))
            print(f"Error creating index '{idxName}' on '{collection.name}': {e}")

    # Check existing indexes by name to avoid duplicates

    existingOrders = orders.index_information()

    print()
    print("Started creating additional indexes (skipping existing)...")

    for idx in ordersAdditionalIndexes:
        if idx.get('options', {}).get('name') not in existingOrders:
            createAndReport(orders, idx)

    print("Finished creating additional indexes.")


if __name__ == '__main__':
    client, db = connectToMongoDB()
    try:
        createIndexes(db)
    finally:
        closeConnection(client)