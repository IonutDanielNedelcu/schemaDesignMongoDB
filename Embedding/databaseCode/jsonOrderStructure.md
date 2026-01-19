# Order JSON Structure

Matches `collectionsStructures/ordersStructure.json`.

Top-level fields and types:

- `_id`: ObjectId
- `orderDate`: Date
- `total`: Number
- `status`: String
- `user`: object (user snapshot)
  - `userIdSnapshot`: ObjectId
  - `usernameSnapshot`: String
  - `emailSnapshot`: String
- `shippingDetails`: object
  - `address`: object (street, city, county, zipcode, country, fullAddress)
  - `method`: String
  - `trackingCode`: String
- `items`: array of objects
  - each item:
    - `productId`: ObjectId
    - `productNameSnapshot`: String
    - `quantity`: Number
    - `unitPriceSnapshot`: Number
    - `skuSnapshot`: String
    - `vendorIdSnapshot`: ObjectId

