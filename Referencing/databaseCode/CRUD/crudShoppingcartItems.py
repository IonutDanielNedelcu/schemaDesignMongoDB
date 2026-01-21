import json
import os
from bson import ObjectId
from connection import connectToMongoDB, closeConnection
from jsonLoader import loadJsonFile

DB_NAME_DEFAULT = "E-Commerce_Ref"


def toObjectId(val):
    try:
        if isinstance(val, ObjectId):
            return val
        if isinstance(val, str) and len(val) == 24:
            return ObjectId(val)
    except Exception:
        pass
    return val


def createShoppingcartItem(item, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return None
    try:
        res = db.shoppingCartItems.insert_one(item)
        return res.inserted_id
    finally:
        closeConnection(client)


def getShoppingcartItemById(itemId, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return None
    try:
        return db.shoppingCartItems.find_one({"_id": toObjectId(itemId)})
    finally:
        closeConnection(client)


def findShoppingcartItems(projection=None, skip=0, limit=100, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return []
    try:
        cursor = db.shoppingCartItems.find({}, projection)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
    finally:
        closeConnection(client)


def updateShoppingcartItemById(itemId, updateFields, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return 0
    try:
        res = db.shoppingCartItems.update_one({"_id": toObjectId(itemId)}, {"$set": updateFields})
        return res.modified_count
    finally:
        closeConnection(client)


def deleteShoppingcartItemById(itemId, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return 0
    try:
        res = db.shoppingCartItems.delete_one({"_id": toObjectId(itemId)})
        return res.deleted_count
    finally:
        closeConnection(client)


def main():
    print("ShoppingCartItems CLI - Referencing")
    print("1) Create shoppingCartItem")
    print("2) Get shoppingCartItem by _id")
    print("3) Find shoppingCartItems (enter JSON filter)")
    print("4) Update shoppingCartItem by _id")
    print("5) Delete shoppingCartItem by _id")
    print("6) Exit")

    choice = input("Choose action (1-6): ").strip()

    if choice == '1':
        print('Using input.json in repository')
        try:
            doc = loadJsonFile('input.json')
            _id = createShoppingcartItem(doc)
            print('Inserted _id:', _id)
        except Exception as e:
            print('Invalid JSON or insert error:', e)

    elif choice == '2':
        _id = input('Enter shoppingCartItem _id: ').strip()
        doc = getShoppingcartItemById(_id)
        print(json.dumps(doc, indent=2, default=str))

    elif choice == '3':
        limit_s = input('Enter result limit (default 10): ').strip()
        try:
            lim = int(limit_s) if limit_s else 10
        except Exception:
            lim = 10
        docs = findShoppingcartItems(limit=lim)
        print(f'Found {len(docs)} documents (showing up to {lim})')
        print(json.dumps(docs[:lim], indent=2, default=str))

    elif choice == '4':
        _id = input('Enter shoppingCartItem _id to update: ').strip()
        print('Using input.json in repository for update')
        try:
            upd = loadJsonFile('input.json')
            modified = updateShoppingcartItemById(_id, upd)
            print('Modified count:', modified)
        except Exception as e:
            print('Invalid JSON or update error:', e)

    elif choice == '5':
        _id = input('Enter shoppingCartItem _id to delete: ').strip()
        deleted = deleteShoppingcartItemById(_id)
        print('Deleted count:', deleted)

    else:
        print('Exiting')


if __name__ == '__main__':
    main()