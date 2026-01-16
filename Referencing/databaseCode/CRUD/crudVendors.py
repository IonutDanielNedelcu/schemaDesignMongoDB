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


def createVendor(vendor, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return None
    try:
        res = db.vendors.insert_one(vendor)
        return res.inserted_id
    finally:
        closeConnection(client)


def getVendorById(vendorId, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return None
    try:
        return db.vendors.find_one({"_id": toObjectId(vendorId)})
    finally:
        closeConnection(client)


def findVendors(projection=None, skip=0, limit=100, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return []
    try:
        cursor = db.vendors.find({}, projection)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
    finally:
        closeConnection(client)


def updateVendorById(vendorId, updateFields, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return 0
    try:
        res = db.vendors.update_one({"_id": toObjectId(vendorId)}, {"$set": updateFields})
        return res.modified_count
    finally:
        closeConnection(client)


def deleteVendorById(vendorId, dbName=DB_NAME_DEFAULT):
    client, db = connectToMongoDB(dbName)
    if db is None:
        return 0
    try:
        res = db.vendors.delete_one({"_id": toObjectId(vendorId)})
        return res.deleted_count
    finally:
        closeConnection(client)


def main():
    print("Vendors CLI - Referencing")
    print("1) Create vendor")
    print("2) Get vendor by _id")
    print("3) Find vendors (enter JSON filter)")
    print("4) Update vendor by _id")
    print("5) Delete vendor by _id")
    print("6) Exit")

    choice = input("Choose action (1-6): ").strip()

    if choice == '1':
        print('Using input.json in repository')
        try:
            doc = loadJsonFile('input.json')
            _id = createVendor(doc)
            print('Inserted _id:', _id)
        except Exception as e:
            print('Invalid JSON or insert error:', e)

    elif choice == '2':
        _id = input('Enter vendor _id: ').strip()
        doc = getVendorById(_id)
        print(json.dumps(doc, indent=2, default=str))

    elif choice == '3':
        limit_s = input('Enter result limit (default 10): ').strip()
        try:
            lim = int(limit_s) if limit_s else 10
        except Exception:
            lim = 10
        docs = findVendors(limit=lim)
        print(f'Found {len(docs)} documents (showing up to {lim})')
        print(json.dumps(docs[:lim], indent=2, default=str))

    elif choice == '4':
        _id = input('Enter vendor _id to update: ').strip()
        print('Using input.json in repository for update')
        try:
            upd = loadJsonFile('input.json')
            modified = updateVendorById(_id, upd)
            print('Modified count:', modified)
        except Exception as e:
            print('Invalid JSON or update error:', e)

    elif choice == '5':
        _id = input('Enter vendor _id to delete: ').strip()
        deleted = deleteVendorById(_id)
        print('Deleted count:', deleted)

    else:
        print('Exiting')


if __name__ == '__main__':
    main()
