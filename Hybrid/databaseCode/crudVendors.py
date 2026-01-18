import json
import os
from pathlib import Path
from connection import connectToMongoDB, closeConnection


DB_NAME_DEFAULT = "eCommerceProjectHybrid"


def createVendor(vendor, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return None
    try:
        res = db.vendors.insert_one(vendor)
        return res.inserted_id
    finally:
        closeConnection(client)


def getVendorById(vendorId, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return None
    try:
        return db.vendors.find_one({"_id": vendorId})
    finally:
        closeConnection(client)


def findVendors(dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return []
    try:
        return list(db.vendors.find({}))
    finally:
        closeConnection(client)


def updateVendorById(vendorId, updateFields, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return 0
    try:
        res = db.vendors.update_one({"_id": vendorId}, {"$set": updateFields})
        return res.modified_count
    finally:
        closeConnection(client)


def deleteVendorById(vendorId, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if not db:
        return 0
    try:
        res = db.vendors.delete_one({"_id": vendorId})
        return res.deleted_count
    finally:
        closeConnection(client)


def main():
    print("Vendors CLI")
    print("1) Create vendor")
    print("2) Get vendor by _id")
    print("3) List all vendors")
    print("4) Update vendor by _id")
    print("5) Delete vendor by _id")
    print("6) Exit")

    choice = input("Choose action (1-6): ").strip()

    if choice == '1':
        print('Using input.json in repository')
        try:
            path = Path(__file__).parent / 'input.json'
            with open(path, 'r', encoding='utf-8') as f:
                doc = json.load(f)
            idInserted = createVendor(doc)
            print('Inserted _id:', idInserted)
        except Exception as e:
            print('Invalid JSON or insert error:', e)

    elif choice == '2':
        idInput = input('Enter vendor _id: ').strip()
        doc = getVendorById(idInput)
        print(json.dumps(doc, indent=2, default=str))

    elif choice == '3':
        docs = findVendors()
        print(f'Found {len(docs)} documents')
        print(json.dumps(docs, indent=2, default=str))

    elif choice == '4':
        idInput = input('Enter vendor _id to update: ').strip()
        print('Using input.json in repository for update')
        try:
            path = Path(__file__).parent / 'input.json'
            with open(path, 'r', encoding='utf-8') as f:
                upd = json.load(f)
            modified = updateVendorById(idInput, upd)
            print('Modified count:', modified)
        except Exception as e:
            print('Invalid JSON or update error:', e)

    elif choice == '5':
        idInput = input('Enter vendor _id to delete: ').strip()
        deleted = deleteVendorById(idInput)
        print('Deleted count:', deleted)

    else:
        print('Exiting')


if __name__ == '__main__':
    main()
