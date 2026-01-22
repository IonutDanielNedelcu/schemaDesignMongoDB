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
  - `specs`: object (free-form product specifications)
- `reviews`: array of objects
  - each review:
    - `userId`: ObjectId
    - `username`: String
    - `rating`: Number
    - `comment`: String
    - `date`: Date

