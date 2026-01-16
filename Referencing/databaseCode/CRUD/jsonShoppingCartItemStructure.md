# ShoppingCartItem JSON Structure

Top-level fields and types for `shoppingCartItems` documents in Referencing Database:

- `_id`: ObjectId
- `productId`: ObjectId - reference to `products` collection
- `quantity`: number

Notes: Ensure `productId` exist before inserting shopping cart item.