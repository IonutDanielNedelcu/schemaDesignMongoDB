# User JSON Structure

Top-level fields and types for user documents:

- `_id`: string (ObjectId hex string) or ObjectId
- `username`: string
- `email`: string
- `addresses`: array of objects
  - each address object:
    - `street`: string
    - `city`: string
    - `county`: string
    - `zipcode`: string
    - `country`: string
    - `fullAddress`: string
- `shoppingCart`: array of objects
  - each cart item:
    - `productName`: string
    - `sku`: string
    - `price`: number
    - `quantity`: integer

Notes: `addresses` and `shoppingCart` can be empty arrays.
