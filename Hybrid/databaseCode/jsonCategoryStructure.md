# Category JSON Structure

Top-level fields and types for category documents:


Example:

```
{
  "_id": "60f7a3c4e13b1f6d5e8a1b2c",
  "name": "Electronics",
  "parentCategoryId": null
}
```
# Category JSON Structure

Matches `collectionsStructures/categoriesStructure.json`.

Top-level fields and types:

- `_id`: ObjectId
- `name`: String
- `parentCategoryId`: ObjectId or null

Notes: use `parentCategoryId` to model hierarchical categories (null indicates a top-level category).
