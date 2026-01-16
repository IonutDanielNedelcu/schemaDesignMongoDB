# OrderItem JSON Structure

Top-level fields and types for `orderItems` documents in Referencing Database:

- `_id`: ObjectId
- `orderId`: ObjectId - reference to `orders` collection
- `productId`: ObjectId - reference to `products` collection
- `vendorId`: ObjectId - reference to `vendors` collection
- `quantity`: number

Notes: Ensure `orderId`, `productId` and `vendorID` exist before inserting order items.