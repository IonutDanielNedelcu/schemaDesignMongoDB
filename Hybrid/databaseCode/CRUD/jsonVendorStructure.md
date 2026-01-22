# Vendor JSON Structure

Top-level fields and types for vendor documents:

Matches `collectionsStructures/vendorsStructure.json`.

Top-level fields and types:

- `_id`: ObjectId
- `companyName`: String
- `contactEmail`: String
- `supportPhone`: String

Notes: vendor documents store basic contact and support information for a vendor. Vendors are referenced by `vendorId` in `products`.

Vendors are referenced by `vendorId` in `products` and may be used to resolve supplier information when populating orders.
