# Modelo de Datos (Iteración 1: Autenticación)

**Nota de Diseño:** Se utiliza UUIDv7 para la Clave Primaria. Esto permite mantener la base de datos indexada eficientemente por tiempo, evitando la fragmentación que producen los UUIDv4 aleatorios.

```mermaid
erDiagram
    users {
        UUID id PK "UUIDv7 (Time-sortable)"
        VARCHAR email UK "Unique, Not Null"
        VARCHAR hashed_password "Not Null"
        VARCHAR role "Default: 'client'"
        BOOLEAN is_active "Default: true"
        TIMESTAMP created_at "Default: now()"
    }