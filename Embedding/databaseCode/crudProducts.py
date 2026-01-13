import json
from .connection import connectToMongoDB, closeConnection


DB_NAME_DEFAULT = "eCommerceProjectEmbedding"


def createProduct(product, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return None
    try:
        res = db.products.insert_one(product)
        return res.inserted_id
    finally:
        closeConnection(client)


def getProductById(prod_id, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return None
    try:
        return db.products.find_one({"_id": prod_id})
    finally:
        closeConnection(client)


def findProducts(projection=None, skip=0, limit=100, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return []
    try:
        cursor = db.products.find({}, projection)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
    finally:
        closeConnection(client)


def updateProductById(prod_id, update_fields, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return 0
    try:
        res = db.products.update_one({"_id": prod_id}, {"$set": update_fields})
        return res.modified_count
    finally:
        closeConnection(client)


def deleteProductById(prod_id, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return 0
    try:
        res = db.products.delete_one({"_id": prod_id})
        return res.deleted_count
    finally:
        closeConnection(client)


def main():
    print("Products CLI")
    print("1) Create product")
    print("2) Get product by _id")
    print("3) Find products (enter JSON filter)")
    print("4) Update product by _id")
    print("5) Delete product by _id")
    print("6) Exit")

    choice = input("Choose action (1-6): ").strip()

    if choice == '1':
        s = input('Enter product JSON: ').strip()
        try:
            doc = json.loads(s)
            _id = createProduct(doc)
            print('Inserted _id:', _id)
        except Exception as e:
            print('Invalid JSON or insert error:', e)

    elif choice == '2':
        _id = input('Enter product _id: ').strip()
        doc = getProductById(_id)
        print(json.dumps(doc, indent=2, default=str))

    elif choice == '3':
        limit_s = input('Enter result limit (default 10): ').strip()
        try:
            lim = int(limit_s) if limit_s else 10
        except Exception:
            lim = 10
        docs = findProducts(limit=lim)
        print(f'Found {len(docs)} documents (showing up to {lim})')
        print(json.dumps(docs[:lim], indent=2, default=str))

    elif choice == '4':
        _id = input('Enter product _id to update: ').strip()
        s = input('Enter JSON with fields to set: ').strip()
        try:
            upd = json.loads(s)
            modified = updateProductById(_id, upd)
            print('Modified count:', modified)
        except Exception as e:
            print('Invalid JSON or update error:', e)

    elif choice == '5':
        _id = input('Enter product _id to delete: ').strip()
        deleted = deleteProductById(_id)
        print('Deleted count:', deleted)

    else:
        print('Exiting')


if __name__ == '__main__':
    main()
