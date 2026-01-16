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


def createOrder(order, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return None
    try:
        res = db.orders.insert_one(order)
        return res.inserted_id
    finally:
        closeConnection(client)


def getOrderById(orderId, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return None
    try:
        return db.orders.find_one({"_id": toObjectId(orderId)})
    finally:
        closeConnection(client)


def findOrders(projection=None, skip=0, limit=100, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return []
    try:
        cursor = db.orders.find({}, projection)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
    finally:
        closeConnection(client)


def updateOrderById(orderId, updateFields, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return 0
    try:
        res = db.orders.update_one({"_id": toObjectId(orderId)}, {"$set": updateFields})
        return res.modified_count
    finally:
        closeConnection(client)


def deleteOrderById(orderId, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return 0
    try:
        res = db.orders.delete_one({"_id": toObjectId(orderId)})
        return res.deleted_count
    finally:
        closeConnection(client)


def main():
    print("Orders CLI - Referencing")
    print("1) Create order")
    print("2) Get order by _id")
    print("3) Find orders (enter JSON filter)")
    print("4) Update order by _id")
    print("5) Delete order by _id")
    print("6) Exit")

    choice = input("Choose action (1-6): ").strip()

    if choice == '1':
        print('Using input.json in repository')
        try:
            doc = loadJsonFile('input.json')
            _id = createOrder(doc)
            print('Inserted _id:', _id)
        except Exception as e:
            print('Invalid JSON or insert error:', e)

    elif choice == '2':
        _id = input('Enter order _id: ').strip()
        doc = getOrderById(_id)
        print(json.dumps(doc, indent=2, default=str))

    elif choice == '3':
        limit_s = input('Enter result limit (default 10): ').strip()
        try:
            lim = int(limit_s) if limit_s else 10
        except Exception:
            lim = 10
        docs = findOrders(limit=lim)
        print(f'Found {len(docs)} documents (showing up to {lim})')
        print(json.dumps(docs[:lim], indent=2, default=str))

    elif choice == '4':
        _id = input('Enter order _id to update: ').strip()
        print('Using input.json in repository for update')
                try:
                    upd = loadJsonFile('input.json')
                    modified = updateOrderById(_id, upd)
            print('Modified count:', modified)
        except Exception as e:
            print('Invalid JSON or update error:', e)

    elif choice == '5':
        _id = input('Enter order _id to delete: ').strip()
        deleted = deleteOrderById(_id)
        print('Deleted count:', deleted)

    else:
        print('Exiting')


if __name__ == '__main__':
    main()
