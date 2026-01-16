# Order JSON Structure

Top-level fields and types for order documents:

- `_id`: string (ObjectId hex string) or ObjectId
- `orderDate`: ISO 8601 string (e.g. `2022-06-16T20:04:22`)
- `total`: number (float)
- `status`: string (e.g. `Pending`, `Delivered`)
- `customerSnapshot`: object
  - `_id`: string/ObjectId
  - `username`: string
  - `email`: string
  - `addresses`: array of address objects (see `jsonUserStructure`)
  - `shoppingCart`: array of cart item objects
- `shippingDetails`: object
  - `address`: address object
  - `method`: string
  - `trackingCode`: string
- `items`: array of objects
  - each item:
    - `productName`: string
    - `sku`: string
    - `unitPrice`: number
    - `quantity`: integer
    - `vendor`: object (companyName, contactEmail, supportPhone)

Notes: `customerSnapshot` is a denormalized snapshot of the user at order time.
