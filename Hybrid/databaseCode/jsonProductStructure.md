
# Product JSON Structure

Matches `collectionsStructures/productsStructure.json`.

Top-level fields and types:

- `_id`: ObjectId
- `name`: String
- `sku`: String
- `price`: Number
- `stock`: Number
- `vendorId`: ObjectId
- `mainCategoryId`: ObjectId
- `subCategoryId`: ObjectId
- `details`: object
  - `description`: String
  - `specs`: object (see note in JSON: copy specs from database products)
- `reviews`: array of objects
  - each review contains:
    - `userId`: ObjectId
    - `username`: String
    - `rating`: Number
    - `comment`: String
    - `date`: Date

Note: `specs` should reflect the product specification fields used in your product documents.
