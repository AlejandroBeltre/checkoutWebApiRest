# checkoutWebApiRest

Este repositorio contiene una API REST en Django para el consumo del paquete pip de la kataCheckout.

## Configuración del Entorno

### Prerrequisitos
- Docker
- Docker Compose (opcional, pero recomendado)

### Instalación y Ejecución

1. Clone el repositorio:
   ```
   git clone https://github.com/yourusername/checkoutWebApiRest.git
   cd checkoutWebApiRest
   ```

2. Ejecute la aplicación usando Docker:
   ```
   docker pull alejandrxbeltre/checkoutwebapi:latest
   docker run -d -p 8000:8000 alejandrxbeltre/checkoutwebapi:latest
   ```

   O si prefiere construir la imagen localmente:
   ```
   docker build -t checkoutwebapi:latest .
   docker run -d -p 8000:8000 checkoutwebapi:latest
   ```

3. La API estará disponible en `http://localhost:8000/`

## Documentación de la API

### Base URL

`http://localhost:8000/`

### Documentación Swagger

La documentación detallada de la API está disponible en Swagger UI:

`http://localhost:8000/docs/`

### Endpoints

#### Checkouts

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET    | `/checkouts/` | Listar todos los checkouts |
| POST   | `/checkouts/` | Crear un nuevo checkout |
| GET    | `/checkouts/{id}/` | Obtener detalles de un checkout específico |
| PUT    | `/checkouts/{id}/` | Actualizar un checkout específico |
| PATCH  | `/checkouts/{id}/` | Actualizar parcialmente un checkout |
| DELETE | `/checkouts/{id}/` | Eliminar un checkout |
| POST   | `/checkouts/{id}/manage_checkout/` | Gestionar un checkout (escanear productos, añadir reglas, calcular total) |

##### Ejemplo de Gestión de Checkout

```json
POST /checkouts/{id}/manage_checkout/
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

#### Productos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET    | `/products/` | Listar todos los productos |
| POST   | `/products/` | Crear un nuevo producto |
| GET    | `/products/{id}/` | Obtener detalles de un producto |
| PUT    | `/products/{id}/` | Actualizar un producto |
| PATCH  | `/products/{id}/` | Actualizar parcialmente un producto |
| DELETE | `/products/{id}/` | Eliminar un producto |

#### Reglas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET    | `/rules/` | Listar todas las reglas |
| POST   | `/rules/` | Crear una nueva regla |
| GET    | `/rules/{id}/` | Obtener detalles de una regla |
| PUT    | `/rules/{id}/` | Actualizar una regla |
| PATCH  | `/rules/{id}/` | Actualizar parcialmente una regla |
| DELETE | `/rules/{id}/` | Eliminar una regla |

### Modelos de Datos

#### Producto
- `product_name` (string): Nombre del producto (único, max 100 caracteres)
- `price` (int): Precio del producto

#### Regla
- `product_name` (string): Nombre del producto (max 100 caracteres)
- `quantity` (int, nullable): Cantidad para la regla
- `discount` (int, nullable): Descuento para la regla

#### Checkout
- `scanned_products` (array): Lista de productos escaneados
- `rules` (array): Lista de reglas aplicadas

#### Producto Escaneado
- `checkout` (int): ID del checkout asociado
- `product` (int): ID del producto escaneado
- `quantity` (int): Cantidad del producto escaneado

## Desarrollo

Para contribuir al proyecto:

1. Fork el repositorio
2. Cree una nueva rama (`git checkout -b feature/AmazingFeature`)
3. Haga commit de sus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abra un Pull Request

## Notas Adicionales

- Todas las solicitudes POST y PUT esperan cuerpos de solicitud en formato JSON, excepto el POST del checkout.
- Las respuestas se devuelven en formato JSON.
- Asegúrese de manejar los errores adecuadamente en su aplicación cliente.

## Soporte

Si encuentra algún problema o tiene alguna pregunta, por favor abra un issue en el repositorio de GitHub.

## Licencia

[Incluya aquí la información de la licencia]
