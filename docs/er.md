# Modelo de Datos (Iteración actual)

**Nota de Diseño:** Se utiliza UUIDv7 para la Clave Primaria. Esto permite mantener la base de datos indexada eficientemente por tiempo, evitando la fragmentación que producen los UUIDv4 aleatorios.

```mermaid
erDiagram
    user {
        UUID user_id PK "UUIDv7"
        VARCHAR email UK "Unique"
        VARCHAR hashed_password
        VARCHAR role
        BOOLEAN is_active
        DATETIME created_at
        DATETIME updated_at
    }

    category {
        UUID category_id PK "UUIDv7"
        VARCHAR name UK
        VARCHAR code UK "Ej: GPU"
        BOOLEAN is_active
        DATETIME created_at
        DATETIME updated_at
    }

    brand {
        UUID brand_id PK "UUIDv7"
        VARCHAR name UK
        VARCHAR code UK "Ej: ASU"
        BOOLEAN is_active
        DATETIME created_at
        DATETIME updated_at
    }

    product {
        UUID product_id PK "UUIDv7"
        VARCHAR name UK "Unique, Index"
        VARCHAR model_slug UK "Unique, Index"
        TEXT description
        UUID category_id FK
        UUID brand_id FK
        BOOLEAN is_active
        DATETIME created_at
        DATETIME updated_at
    }

    %% Relaciones
    category ||--|{ product : "clasifica a"
    brand    ||--|{ product : "fabrica a"