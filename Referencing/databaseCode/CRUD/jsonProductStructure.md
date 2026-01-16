# Product JSON Structure

Top-level fields and types for `products` documents in Referencing Database:

- `_id`: ObjectId
- `name`: string 
- `sku`: string 
- `price`: number
- `stock`: number
- `vendorId`: ObjectId - reference to `vendors` collection
- `mainCategoryId`: ObjectId - reference to `categories` collection
- `subCategoryId`: ObjectId - reference to `categories` collection
- `details`: object
    - `description`: string
    - `specs`: object

Notes: Ensure `mainCategoryId`, `subCategoryId` and `vendorId` references exist in their collections before linking products.