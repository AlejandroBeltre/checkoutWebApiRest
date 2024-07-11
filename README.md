# checkoutWebApiRest
Repositorio para el consumo del paquete de pip de la kataCheckout en una web api rest en django con python.

## Base URL

`/localhost:8000/`

## Docs URL
`/localhost:8000/docs/`

## Endpoints

### Checkouts

#### List Checkouts
- **URL:** `/checkouts/`
- **Method:** GET
- **Description:** Retrieve a list of all checkouts.

#### Create Checkout
- **URL:** `/checkouts/`
- **Method:** POST
- **Description:** Create a new checkout.

#### Retrieve Checkout
- **URL:** `/checkouts/{id}/`
- **Method:** GET
- **Description:** Retrieve details of a specific checkout.

#### Update Checkout
- **URL:** `/checkouts/{id}/`
- **Method:** PUT
- **Description:** Update a specific checkout.

#### Partial Update Checkout
- **URL:** `/checkouts/{id}/`
- **Method:** PATCH
- **Description:** Partially update a specific checkout.

#### Delete Checkout
- **URL:** `/checkouts/{id}/`
- **Method:** DELETE
- **Description:** Delete a specific checkout.

#### Manage Checkout
- **URL:** `/checkouts/{id}/manage_checkout/`
- **Method:** POST
- **Description:** Manage a checkout, including scanning products, adding rules, and calculating totals.
- **Parameters:**
  - `action_type` (string): Type of action to perform (e.g., "manage_checkout")
  - `scan_product` (object, optional): Product to scan
    - `product_name` (string): Name of the product
    - `quantity` (integer, optional): Quantity of the product (default: 1)
  - `add_rule` (object, optional): Rule to add
    - `rule_id` (integer): ID of the rule to add
  - `total` (boolean, optional): Calculate total if set to true

### Products

#### List Products
- **URL:** `/products/`
- **Method:** GET
- **Description:** Retrieve a list of all products.

#### Create Product
- **URL:** `/products/`
- **Method:** POST
- **Description:** Create a new product.

#### Retrieve Product
- **URL:** `/products/{id}/`
- **Method:** GET
- **Description:** Retrieve details of a specific product.

#### Update Product
- **URL:** `/products/{id}/`
- **Method:** PUT
- **Description:** Update a specific product.

#### Partial Update Product
- **URL:** `/products/{id}/`
- **Method:** PATCH
- **Description:** Partially update a specific product.

#### Delete Product
- **URL:** `/products/{id}/`
- **Method:** DELETE
- **Description:** Delete a specific product.

### Rules

#### List Rules
- **URL:** `/rules/`
- **Method:** GET
- **Description:** Retrieve a list of all rules.

#### Create Rule
- **URL:** `/rules/`
- **Method:** POST
- **Description:** Create a new rule.

#### Retrieve Rule
- **URL:** `/rules/{id}/`
- **Method:** GET
- **Description:** Retrieve details of a specific rule.

#### Update Rule
- **URL:** `/rules/{id}/`
- **Method:** PUT
- **Description:** Update a specific rule.

#### Partial Update Rule
- **URL:** `/rules/{id}/`
- **Method:** PATCH
- **Description:** Partially update a specific rule.

#### Delete Rule
- **URL:** `/rules/{id}/`
- **Method:** DELETE
- **Description:** Delete a specific rule.

## Models

### Product
- `product_name` (string): Name of the product (unique, max length: 100)
- `price` (integer): Price of the product

### Rule
- `product_name` (string): Name of the product (max length: 100)
- `quantity` (integer, nullable): Quantity for the rule
- `discount` (integer, nullable): Discount for the rule

### Checkout
- `scanned_products` (array): List of scanned products
- `rules` (array): List of applied rules

### ScannedProduct
- `checkout` (integer): ID of the associated checkout
- `product` (integer): ID of the scanned product
- `quantity` (integer): Quantity of the scanned product

## Notes

- All POST and PUT requests expect JSON-formatted request bodies.
- Responses are returned in JSON format.
- Authentication may be required for certain endpoints (not specified in the provided code).
