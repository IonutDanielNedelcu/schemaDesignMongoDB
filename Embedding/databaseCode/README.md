# Database Setup

## Files/Directories:
    1. 1populateProducts.py -> product generator script (initial dataset). Uploads to 'products' collection.
    2. 1populateProducts2.py -> additional product generator (more sample products).
    3. 2populateUsers.py -> user generator script. Uploads to 'users' collection.
    4. 3populateOrders.py -> orders RANDOM generator script. Uploads to 'orders' collection. (running this multiple times gives different data)
    5. connection.py -> MongoDB connection helper used by the scripts.
    6. crudOrders -> basic CRUD operations on 'orders' collection. Uses 'input.json' for input data.
    7. crudProducts -> basic CRUD operations on 'products' collection. Uses 'input.json' for input data.
    8. crudUsers -> basic CRUD operations on 'users' collection. Uses 'input.json' for input data.
    9. input.json -> input file for CRUD operations.
    10. jsonLoader.py -> helper script for uploading data from 'input.json' to CRUD operations.
    11. jsonOrderStructure.md -> markdown helper guide for 'orders' CRUD data input.
    12. jsonProductStructure.md -> markdown helper guide for 'products' CRUD data input.
    13. jsonUserSructure.md -> markdown helper guide for 'users' CRUD data input.
    14. MongoToJsonOrders.py -> takes data from 'orders' collection in MongoDB Atlas and loads it to 'sharding' folder (external), 'JsonOrders' subfolder, in a .json format.
    14. MongoToJsonProducts.py -> takes data from 'products' collection in MongoDB Atlas and loads it to 'sharding' folder (external), 'JsonProducts' subfolder, in a .json format.
    14. MongoToJsonUsers.py -> takes data from 'users' collection in MongoDB Atlas and loads it to 'sharding' folder (external), 'JsonUsers' subfolder, in a .json format.


## Usage Steps:
    1. Create the .env file and add the environment variables mentioned in Notes.
    2. Run the database populating scripts in the next order: '1populateProducts.py', '1populateProducts2.py', '2populateUsers.py', '3populateOrders.py' (they automatically connect to the database through 'connection.py').
    3. (Optional) Play with CRUD operations and scripts.
    4. Run the database .json saving converters for a future step (sharding).


### Notes:
    1. A .env file is needed, with the next environment variables:
        a. MONGO_CONNECTION_STRING -> connection string for the MongoDB Atlas Database.
