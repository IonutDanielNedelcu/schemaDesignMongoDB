# Order JSON Structure

Top-level fields and types for `orders` documents in Referencing Database:

- `_id`: ObjectId
- `orderDate`: ISO 8601 string (e.g. `2022-06-16T20:04:22`)
- `total`: number
- `status`: string - `pending`, `processing`, `shipped`, `delivered`, `cancelled`
- `userId`: ObjectId - reference to `users` collection
- `shippingAddressId`: ObjectId - reference to `addresses`
- `shippingDetails`: object
    - `method`: string
    - `trackingCode`: string