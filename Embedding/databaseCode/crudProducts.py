import json
import os
from .connection import connectToMongoDB, closeConnection
from .jsonLoader import loadJsonFile


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


def getProductById(prodId, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return None
    try:
        return db.products.find_one({"_id": prodId})
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


def updateProductById(prodId, updateFields, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return 0
    try:
        res = db.products.update_one({"_id": prodId}, {"$set": updateFields})
        return res.modified_count
    finally:
        closeConnection(client)


def deleteProductById(prodId, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return 0
    try:
        res = db.products.delete_one({"_id": prodId})
        return res.deleted_count
    finally:
        closeConnection(client)


def main():
    print("Products CLI")
    print("1) Create product")
    print("2) Get product by _id")
    print("3) List all products")
    print("4) Update product by _id")
    print("5) Delete product by _id")
    print("6) Exit")

    choice = input("Choose action (1-6): ").strip()

    if choice == '1':
        print('Using input.json in repository')
        try:
            path = os.path.join(os.path.dirname(__file__), 'input.json')
            doc = loadJsonFile(path)
            idInserted = createProduct(doc)
            print('Inserted _id:', idInserted)
        except Exception as e:
            print('Invalid JSON or insert error:', e)

    elif choice == '2':
        idInput = input('Enter product _id: ').strip()
        doc = getProductById(idInput)
        print(json.dumps(doc, indent=2, default=str))

    elif choice == '3':
        docs = findProducts(limit=0)
        print(f'Found {len(docs)} documents')
        print(json.dumps(docs, indent=2, default=str))

    elif choice == '4':
        idInput = input('Enter product _id to update: ').strip()
        print('Using input.json in repository for update')
        try:
            path = os.path.join(os.path.dirname(__file__), 'input.json')
            upd = loadJsonFile(path)
            modified = updateProductById(idInput, upd)
            print('Modified count:', modified)
        except Exception as e:
            print('Invalid JSON or update error:', e)

    elif choice == '5':
        idInput = input('Enter product _id to delete: ').strip()
        deleted = deleteProductById(idInput)
        print('Deleted count:', deleted)

    else:
        print('Exiting')


if __name__ == '__main__':
    main()
