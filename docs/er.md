# Modelo de Datos (Iteración actual)

**Nota de Diseño:** Se utiliza UUIDv7 para la Clave Primaria. Esto permite mantener la base de datos indexada eficientemente por tiempo, evitando la fragmentación que producen los UUIDv4 aleatorios.

```mermaid
erDiagram
    user {
        UUID user_id PK "UUIDv7"
        VARCHAR email UK "Unique"
        VARCHAR hashed_password
        VARCHAR role "Default: client"
        BOOLEAN is_active "Default: True"
        DATETIME created_at
        DATETIME updated_at
    }

    category {
        UUID category_id PK "UUIDv7"
        VARCHAR name UK
        VARCHAR code UK "Ej: GPU"
        BOOLEAN is_active "Default: True"
        DATETIME created_at
        DATETIME updated_at
    }

    brand {
        UUID brand_id PK "UUIDv7"
        VARCHAR name UK
        VARCHAR code UK "Ej: ASU"
        BOOLEAN is_active "Default: True"
        DATETIME created_at
        DATETIME updated_at
    }

    product {
        UUID product_id PK "UUIDv7"
        VARCHAR name UK "Unique, Index"
        VARCHAR slug UK "Unique, Index"
        TEXT description
        UUID category_id FK
        UUID brand_id FK
        BOOLEAN is_active "Default: True"
        DATETIME created_at
        DATETIME updated_at
    }

    product_variant {
        UUID variant_id PK "UUIDv7"
        UUID product_id FK
        VARCHAR sku UK "Unique"
        DECIMAL price
        INTEGER stock
        BOOLEAN is_active "Default: True"
        DATETIME created_at
        DATETIME updated_at
    }

    product_image {
        UUID image_id PK "UUIDv7"
        VARCHAR image_url
        BOOLEAN is_main "Default: False"
        UUID product_id FK 
        UUID variant_id FK "Nullable"
        DATETIME created_at
        DATETIME updated_at
    }

    %% Relaciones (Corregidas a "Cero o Muchos")
    category ||--o{ product : "clasifica a"
    brand    ||--o{ product : "fabrica a"
    product  ||--o{ product_variant : "tiene variantes"
    
    %% Relaciones de Imágenes
    product         ||--o{ product_image : "tiene fotos genéricas"
    product_variant ||--o{ product_image : "tiene fotos específicas"