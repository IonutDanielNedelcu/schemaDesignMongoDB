# User JSON Structure

Matches `collectionsStructures/usersStructure.json`.

Top-level fields and types:

- `_id`: ObjectId
- `username`: String
- `email`: String
- `addresses`: array of address objects
  - address fields:
    - `street`: String
    - `city`: String
    - `county`: String
    - `zipcode`: String
    - `country`: String
    - `fullAddress`: String
- `shoppingCart`: array of objects
  - each cart item:
    - `productId`: ObjectId
    - `quantity`: Number

Notes: adapt `shoppingCart` to store references or denormalized snapshots as needed by your application.
# User JSON Structure

Top-level fields and types for user documents:

- `_id`: string (ObjectId hex string) or ObjectId
- `username`: string
- `email`: string
- `fullName`: string
- `phone`: string
- `addresses`: array of address objects
  - address object fields: `street`, `city`, `postalCode`, `country`, `isDefault` (boolean)
- `createdAt`: ISO 8601 string or Date
- `shoppingCart`: array of cart item objects
  - cart item fields: `productId` or `sku`, `quantity`, `addedAt`


