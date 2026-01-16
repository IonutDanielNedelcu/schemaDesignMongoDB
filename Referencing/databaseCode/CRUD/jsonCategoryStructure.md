# Category JSON Structure

Top-level fields and types for `categories` documents in Referencing Database:

- `_id`: ObjectId
- `name`: string — category display name (required)
- `parentCategoryId`: ObjectId or null - reference to parent category for hierarchies

Notes: `parentCategoryId` should point to another document in the same `categories` collection or be `null` for top-level categories
