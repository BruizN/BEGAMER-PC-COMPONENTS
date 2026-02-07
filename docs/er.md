# Modelo de Datos (Iteración 1: Autenticación)

**Nota de Diseño:** Se utiliza UUIDv7 para la Clave Primaria. Esto permite mantener la base de datos indexada eficientemente por tiempo, evitando la fragmentación que producen los UUIDv4 aleatorios.

```mermaid
erDiagram
    user {
        UUID user_id PK "UUIDv7 (Time-sortable)"
        VARCHAR email UK "Unique, Not Null"
        VARCHAR hashed_password "Not Null"
        VARCHAR role "Default: 'client'"
        BOOLEAN is_active "Default: true"
        DATETIME created_at "Server Default: now()"
        DATETIME updated_at "OnUpdate: now()"
    }

    category {
        UUID category_id PK "UUIDv7 (Time-sortable)"
        VARCHAR name UK "Unique, Not Null"
        VARCHAR code UK "Unique, Not Null"
        BOOLEAN is_active "Default: true"
        DATETIME created_at "Server Default: now()"
        DATETIME updated_at "OnUpdate: now()"
    }

    brand {
        UUID brand_id PK "UUIDv7 (Time-sortable)"
        VARCHAR name UK "Unique, Not Null"
        VARCHAR code UK "Unique, Not Null"
        BOOLEAN is_active "Default: true"
        DATETIME created_at "Server Default: now()"
        DATETIME updated_at "OnUpdate: now()"
    }