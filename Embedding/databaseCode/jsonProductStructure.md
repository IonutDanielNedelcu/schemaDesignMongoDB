# Product JSON Structure

Top-level fields and types for product documents:

- `_id`: string (ObjectId hex string) or ObjectId
- `name`: string
- `sku`: string
- `price`: number (float)
- `details`: object
  - `description`: string
  - `specs`: object (free-form key/value strings, e.g. `capacity`, `ports`, `weight`)
- `stock`: integer
- `category`: object
  - `main`: string
  - `sub`: string
- `vendor`: object
  - `companyName`: string
  - `contactEmail`: string
  - `supportPhone`: string
- `reviews`: array of objects
  - each review object:
    - `userDisplayName`: string
    - `rating`: integer
    - `comment`: string
    - `date`: ISO 8601 string (e.g. `2020-07-22T00:00:00`)

Notes: fields under `details.specs` and `vendor` are flexible; `reviews` is optional and can be empty.
