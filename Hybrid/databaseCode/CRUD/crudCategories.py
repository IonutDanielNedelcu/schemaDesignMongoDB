import json
import os
from pathlib import Path
from connection import connectToMongoDB, closeConnection


DB_NAME_DEFAULT = "eCommerceProjectHybrid"


def createCategory(category, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return None
    try:
        res = db.categories.insert_one(category)
        return res.inserted_id
    finally:
        closeConnection(client)


def getCategoryById(catId, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return None
    try:
        return db.categories.find_one({"_id": catId})
    finally:
        closeConnection(client)


def findCategories(dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return []
    try:
        return list(db.categories.find({}))
    finally:
        closeConnection(client)


def updateCategoryById(catId, updateFields, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return 0
    try:
        res = db.categories.update_one({"_id": catId}, {"$set": updateFields})
        return res.modified_count
    finally:
        closeConnection(client)


def deleteCategoryById(catId, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return 0
    try:
        res = db.categories.delete_one({"_id": catId})
        return res.deleted_count
    finally:
        closeConnection(client)


def main():
    print("Categories CLI")
    print("1) Create category")
    print("2) Get category by _id")
    print("3) List all categories")
    print("4) Update category by _id")
    print("5) Delete category by _id")
    print("6) Exit")

    choice = input("Choose action (1-6): ").strip()

    if choice == '1':
        print('Using input.json in repository')
        try:
            path = Path(__file__).parent / 'input.json'
            with open(path, 'r', encoding='utf-8') as f:
                doc = json.load(f)
            idInserted = createCategory(doc)
            print('Inserted _id:', idInserted)
        except Exception as e:
            print('Invalid JSON or insert error:', e)

    elif choice == '2':
        idInput = input('Enter category _id: ').strip()
        doc = getCategoryById(idInput)
        print(json.dumps(doc, indent=2, default=str))

    elif choice == '3':
        docs = findCategories()
        print(f'Found {len(docs)} documents')
        print(json.dumps(docs, indent=2, default=str))

    elif choice == '4':
        idInput = input('Enter category _id to update: ').strip()
        print('Using input.json in repository for update')
        try:
            path = Path(__file__).parent / 'input.json'
            with open(path, 'r', encoding='utf-8') as f:
                upd = json.load(f)
            modified = updateCategoryById(idInput, upd)
            print('Modified count:', modified)
        except Exception as e:
            print('Invalid JSON or update error:', e)

    elif choice == '5':
        idInput = input('Enter category _id to delete: ').strip()
        deleted = deleteCategoryById(idInput)
        print('Deleted count:', deleted)

    else:
        print('Exiting')


if __name__ == '__main__':
    main()
