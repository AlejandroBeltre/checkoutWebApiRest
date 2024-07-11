# checkoutWebApiRest
Repositorio para el consumo del paquete de pip de la kataCheckout en una web api rest en django con python.

## Base URL

`/localhost:8000/`

## Docs URL
`/localhost:8000/docs/`

## Endpoints

### Checkouts

#### Listar Checkouts
- **URL:** `/checkouts/`
- **Método:** GET
- **Descripción:** Obtener una lista de todos los checkouts.

#### Crear Checkout
- **URL:** `/checkouts/`
- **Método:** POST
- **Descripción:** Crear un nuevo checkout.

#### Obtener Checkout
- **URL:** `/checkouts/{id}/`
- **Método:** GET
- **Descripción:** Obtener detalles de un checkout específico.

#### Actualizar Checkout
- **URL:** `/checkouts/{id}/`
- **Método:** PUT
- **Descripción:** Actualizar un checkout específico.

#### Actualizar Parcialmente Checkout
- **URL:** `/checkouts/{id}/`
- **Método:** PATCH
- **Descripción:** Actualizar parcialmente un checkout específico.

#### Eliminar Checkout
- **URL:** `/checkouts/{id}/`
- **Método:** DELETE
- **Descripción:** Eliminar un checkout específico.

#### Gestionar Checkout
- **URL:** `/checkouts/{id}/manage_checkout/`
- **Método:** POST
- **Descripción:** Gestionar un checkout, incluyendo escaneo de productos, adición de reglas y cálculo de totales.
- **Parámetros:**
  - `action_type` (string): Tipo de acción a realizar (ej. "manage_checkout")
  - `scan_product` (objeto, opcional): Producto a escanear
    - `product_name` (string): Nombre del producto
    - `quantity` (entero, opcional): Cantidad del producto (por defecto: 1)
  - `add_rule` (objeto, opcional): Regla a añadir
    - `rule_id` (entero): ID de la regla a añadir
  - `total` (booleano, opcional): Calcular total si se establece a verdadero
```
{
    "action_type": "manage_checkout",
    "scan_product": {
        "product_name": "example_product",
        "quantity": 2
    },
    "add_rule": {
        "rule_id": 1
    },
    "total": true
}
```


### Productos

#### Listar Productos
- **URL:** `/products/`
- **Método:** GET
- **Descripción:** Obtener una lista de todos los productos.

#### Crear Producto
- **URL:** `/products/`
- **Método:** POST
- **Descripción:** Crear un nuevo producto.

#### Obtener Producto
- **URL:** `/products/{id}/`
- **Método:** GET
- **Descripción:** Obtener detalles de un producto específico.

#### Actualizar Producto
- **URL:** `/products/{id}/`
- **Método:** PUT
- **Descripción:** Actualizar un producto específico.

#### Actualizar Parcialmente Producto
- **URL:** `/products/{id}/`
- **Método:** PATCH
- **Descripción:** Actualizar parcialmente un producto específico.

#### Eliminar Producto
- **URL:** `/products/{id}/`
- **Método:** DELETE
- **Descripción:** Eliminar un producto específico.

### Reglas

#### Listar Reglas
- **URL:** `/rules/`
- **Método:** GET
- **Descripción:** Obtener una lista de todas las reglas.

#### Crear Regla
- **URL:** `/rules/`
- **Método:** POST
- **Descripción:** Crear una nueva regla.

#### Obtener Regla
- **URL:** `/rules/{id}/`
- **Método:** GET
- **Descripción:** Obtener detalles de una regla específica.

#### Actualizar Regla
- **URL:** `/rules/{id}/`
- **Método:** PUT
- **Descripción:** Actualizar una regla específica.

#### Actualizar Parcialmente Regla
- **URL:** `/rules/{id}/`
- **Método:** PATCH
- **Descripción:** Actualizar parcialmente una regla específica.

#### Eliminar Regla
- **URL:** `/rules/{id}/`
- **Método:** DELETE
- **Descripción:** Eliminar una regla específica.

## Modelos

### Producto
- `product_name` (string): Nombre del producto (unique, longitud máxima: 100)
- `price` (int): Precio del producto

### Regla
- `product_name` (string): Nombre del producto (longitud máxima: 100)
- `quantity` (int, nullable): Cantidad para la regla
- `discount` (int, nullable): Descuento para la regla

### Checkout
- `scanned_products` (array): Lista de productos escaneados
- `rules` (array): Lista de reglas aplicadas

### Producto Escaneado
- `checkout` (int): ID del checkout asociado
- `product` (int): ID del producto escaneado
- `quantity` (int): Cantidad del producto escaneado

## Comentarios

- Todas las solicitudes POST y PUT esperan cuerpos de solicitud en formato JSON, excepto el post del checkout.
- Las respuestas se devuelven en formato JSON.
