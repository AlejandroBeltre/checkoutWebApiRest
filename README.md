# checkoutWebApiRest

Este repositorio contiene una API REST en Django para el consumo del paquete pip de la kataCheckout.

## Configuración del Entorno

### Prerrequisitos
- Docker
- Docker Compose (recomendado)

### Instalación y Ejecución

#### Opción 1: Docker Compose (Recomendado)

1. Clone el repositorio:
   ```bash
   git clone https://github.com/AlejandroBeltre/checkoutWebApiRest.git
   cd checkoutWebApiRest
   ```

2. **Con SQLite (Base de datos por defecto):**
   ```bash
   docker-compose up -d
   ```

   **Con PostgreSQL:**
   ```bash
   docker-compose -f docker-compose.postgres.yml up -d
   ```

3. La API estará disponible en `http://localhost:8000/`
4. Panel de administración: `http://localhost:8000/admin/` (usuario: admin, contraseña: admin123)

#### Opción 2: Docker sin Compose

1. Clone el repositorio:
   ```bash
   git clone https://github.com/AlejandroBeltre/checkoutWebApiRest.git
   cd checkoutWebApiRest
   ```

2. Construya la imagen:
   ```bash
   docker build -t checkoutwebapi:latest .
   ```

3. Ejecute el contenedor:
   ```bash
   # Crear directorio para la base de datos
   mkdir -p data

   # Ejecutar contenedor con SQLite
   docker run -d -p 8000:8000 -v $(pwd)/data:/code/data checkoutwebapi:latest
   ```

4. La API estará disponible en `http://localhost:8000/`

#### Opción 3: Usar imagen pre-construida

```bash
docker pull alejandrxbeltre/checkoutwebapi:latest
docker run -d -p 8000:8000 -v $(pwd)/data:/code/data alejandrxbeltre/checkoutwebapi:latest
```

### Configuración Avanzada

#### Variables de Entorno

Puede personalizar la aplicación usando variables de entorno. Copie `.env.example` a `.env` y modifique según necesite:

```bash
cp .env.example .env
```

Variables disponibles:
- `DJANGO_SECRET_KEY`: Clave secreta de Django (cambiar en producción)
- `DJANGO_DEBUG`: Modo debug (True/False)
- `DJANGO_ALLOWED_HOSTS`: Hosts permitidos (separados por comas)
- `DB_ENGINE`: Motor de base de datos (sqlite3/postgresql)
- `DB_PATH`: Ruta a la base de datos SQLite
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Configuración PostgreSQL

#### Base de Datos

**SQLite (Por defecto):**
- Base de datos local almacenada en `./data/db.sqlite3`
- Ideal para desarrollo y pruebas
- Los datos persisten en el volumen montado

**PostgreSQL (Opcional):**
- Para entornos de producción o desarrollo con mayor carga
- Use `docker-compose.postgres.yml` para despliegue completo
- Configuración automática con variables de entorno

### Gestión del Contenedor

```bash
# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Reconstruir imagen
docker-compose build

# Ejecutar comandos en el contenedor
docker-compose exec web python manage.py <comando>

# Crear migraciones
docker-compose exec web python manage.py makemigrations

# Aplicar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario adicional
docker-compose exec web python manage.py createsuperuser
```

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

## Notas Adicionales

- Todas las solicitudes POST y PUT esperan cuerpos de solicitud en formato JSON, excepto el POST del checkout.
- Las respuestas se devuelven en formato JSON.
- Asegúrese de manejar los errores adecuadamente en su aplicación cliente.

## Soporte

Si encuentra algún problema o tiene alguna pregunta, por favor abra un issue en el repositorio de GitHub.
