import json
import os
from pathlib import Path
from connection import connectToMongoDB, closeConnection


DB_NAME_DEFAULT = "eCommerceProjectHybrid"


def createUser(user, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return None
    try:
        res = db.users.insert_one(user)
        return res.inserted_id
    finally:
        closeConnection(client)


def getUserById(userId, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return None
    try:
        return db.users.find_one({"_id": userId})
    finally:
        closeConnection(client)


def findUsers(dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return []
    try:
        return list(db.users.find({}))
    finally:
        closeConnection(client)


def updateUserById(userId, updateFields, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return 0
    try:
        res = db.users.update_one({"_id": userId}, {"$set": updateFields})
        return res.modified_count
    finally:
        closeConnection(client)


def deleteUserById(userId, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return 0
    try:
        res = db.users.delete_one({"_id": userId})
        return res.deleted_count
    finally:
        closeConnection(client)


def main():
    print("Users CLI")
    print("1) Create user")
    print("2) Get user by _id")
    print("3) List all users")
    print("4) Update user by _id")
    print("5) Delete user by _id")
    print("6) Exit")

    choice = input("Choose action (1-6): ").strip()

    if choice == '1':
        print('Using input.json in repository')
        try:
            path = Path(__file__).parent / 'input.json'
            with open(path, 'r', encoding='utf-8') as f:
                doc = json.load(f)
            idInserted = createUser(doc)
            print('Inserted _id:', idInserted)
        except Exception as e:
            print('Invalid JSON or insert error:', e)

    elif choice == '2':
        idInput = input('Enter user _id: ').strip()
        doc = getUserById(idInput)
        print(json.dumps(doc, indent=2, default=str))

    elif choice == '3':
        docs = findUsers()
        print(f'Found {len(docs)} documents')
        print(json.dumps(docs, indent=2, default=str))

    elif choice == '4':
        idInput = input('Enter user _id to update: ').strip()
        print('Using input.json in repository for update')
        try:
            path = Path(__file__).parent / 'input.json'
            with open(path, 'r', encoding='utf-8') as f:
                upd = json.load(f)
            modified = updateUserById(idInput, upd)
            print('Modified count:', modified)
        except Exception as e:
            print('Invalid JSON or update error:', e)

    elif choice == '5':
        idInput = input('Enter user _id to delete: ').strip()
        deleted = deleteUserById(idInput)
        print('Deleted count:', deleted)

    else:
        print('Exiting')


if __name__ == '__main__':
    main()
