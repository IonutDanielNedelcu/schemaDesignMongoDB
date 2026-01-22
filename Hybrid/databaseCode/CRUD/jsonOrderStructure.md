
# Order JSON Structure

This document describes the order structure from `collectionsStructures/ordersStructure.json`.

Top-level fields and types:

- `_id`: ObjectId
- `orderDate`: Date
- `total`: Number
- `status`: String
- `user`: object containing a denormalized user snapshot:
  - `userIdSnapshot`: ObjectId
  - `usernameSnapshot`: String
  - `emailSnapshot`: String
- `shippingDetails`: object
  - `address`: object
    - `street`: String
    - `city`: String
    - `county`: String
    - `zipcode`: String
    - `country`: String
    - `fullAddress`: String
  - `method`: String
  - `trackingCode`: String
- `items`: array of objects with:
  - `productId`: ObjectId
  - `productNameSnapshot`: String
  - `quantity`: Number
  - `unitPriceSnapshot`: Number
  - `skuSnapshot`: String
  - `vendorIdSnapshot`: ObjectId

Notes: `user` and `items[*]` contain denormalized snapshots to preserve order-time data.
