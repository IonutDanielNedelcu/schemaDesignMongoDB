# User JSON Structure

Top-level fields and types for `users` documents in Referencing Database:

- `_id`: ObjectId
- `username`: string
- `email`: string
- `addresses`: Array of ObjectId (references to `addresses` collection)
- `shoppingCart`: Array of ObjectId (references to `shoppingCartItems` collection)