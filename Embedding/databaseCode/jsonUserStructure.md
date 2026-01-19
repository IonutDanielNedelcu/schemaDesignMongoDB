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
