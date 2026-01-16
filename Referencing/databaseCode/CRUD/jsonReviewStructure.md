# Review JSON Structure

Top-level fields and types for `reviews` documents in Referencing Database:

- `_id`: ObjectId
- `productId`: ObjectId - reference to `products` collection
- `userId`: ObjectId - reference to `users` collection
- `rating`: number
- `comment`: string
- `date`: ISO 8601 string (e.g. `2022-06-16T20:04:22`)

Notes: Ensure `productId` and `userId` exist before inserting reviews