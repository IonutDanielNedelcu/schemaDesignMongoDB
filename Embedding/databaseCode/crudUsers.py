import json
import os
from .connection import connectToMongoDB, closeConnection
from .jsonLoader import loadJsonFile


DB_NAME_DEFAULT = "eCommerceProjectEmbedding"


def createUser(user, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return None
    try:
        res = db.users.insert_one(user)
        return res.inserted_id
    finally:
        closeConnection(client)


def getUserById(user_id, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return None
    try:
        return db.users.find_one({"_id": user_id})
    finally:
        closeConnection(client)


def findUsers(projection=None, skip=0, limit=100, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return []
    try:
        cursor = db.users.find({}, projection)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
    finally:
        closeConnection(client)


def updateUserById(user_id, update_fields, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return 0
    try:
        res = db.users.update_one({"_id": user_id}, {"$set": update_fields})
        return res.modified_count
    finally:
        closeConnection(client)


def deleteUserById(user_id, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return 0
    try:
        res = db.users.delete_one({"_id": user_id})
        return res.deleted_count
    finally:
        closeConnection(client)


def main():
    print("Users CLI")
    print("1) Create user")
    print("2) Get user by _id")
    print("3) Find users (enter JSON filter)")
    print("4) Update user by _id")
    print("5) Delete user by _id")
    print("6) Exit")

    choice = input("Choose action (1-6): ").strip()

    if choice == '1':
        print('Using input.json in repository')
        try:
            path = os.path.join(os.path.dirname(__file__), 'input.json')
            doc = loadJsonFile(path)
            _id = createUser(doc)
            print('Inserted _id:', _id)
        except Exception as e:
            print('Invalid JSON or insert error:', e)

    elif choice == '2':
        _id = input('Enter user _id: ').strip()
        doc = getUserById(_id)
        print(json.dumps(doc, indent=2, default=str))

    elif choice == '3':
        limit_s = input('Enter result limit (default 10): ').strip()
        try:
            lim = int(limit_s) if limit_s else 10
        except Exception:
            lim = 10
        docs = findUsers(limit=lim)
        print(f'Found {len(docs)} documents (showing up to {lim})')
        print(json.dumps(docs[:lim], indent=2, default=str))

    elif choice == '4':
        _id = input('Enter user _id to update: ').strip()
        print('Using input.json in repository for update')
        try:
            path = os.path.join(os.path.dirname(__file__), 'input.json')
            upd = loadJsonFile(path)
            modified = updateUserById(_id, upd)
            print('Modified count:', modified)
        except Exception as e:
            print('Invalid JSON or update error:', e)

    elif choice == '5':
        _id = input('Enter user _id to delete: ').strip()
        deleted = deleteUserById(_id)
        print('Deleted count:', deleted)

    else:
        print('Exiting')


if __name__ == '__main__':
    main()
