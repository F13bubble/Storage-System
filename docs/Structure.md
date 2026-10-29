## Models:
### Item
- id (unique)
- name
- description
- category_id
- manufacturer
- unit
- purchase_price (decimal)
- reorder_limit
- is_active
- created_at
- updated_at
- created_by
- updated_by

### ItemBarcode
- id (PK)
- item_id
- code (unique, string)
- symbology (EAN13, UPCA, CODE128, QR, ...)
- source (MANUFACTURER, INTERNAL)
- pack_quantity (default 1)
- is_primary
- created_at
- created_by

### Stock
- item_id (PK)
- location_id (PK)
- quantity
- updated_at

### StockMovement
- id (PK)
- item_id
- from_location_id
- to_location_id
- quantity
- type
- reason
- created_by
- created_at

### Location
- id (PK)
- code (unique, string)
- name
- description
- parent_id (nullable)
- created_at
- updated_at
- created_by
- updated_by
- is_active

### Category
- id (PK)
- name
- description
- color
- parent_id (nullable)
- is_active

### User
- id (PK)
- firstname
- lastname
- email (unique)
- password_hash
- role_id
- created_at
- updated_at
- last_login_at
- is_active

### Role
- id (PK)
- name
- description
- can_manage_users
- can_edit_items
- can_move_stock
- can_adjust_stock
- created_by
- created_at
- updated_by
- updated_at