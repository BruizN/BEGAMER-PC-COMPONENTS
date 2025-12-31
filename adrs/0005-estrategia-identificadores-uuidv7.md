# 5. Estrategia de Identificadores (Primary Keys): UUIDv7

**Fecha:** 2025-12-31
**Estado:** Aceptado

## Contexto
El sistema requiere identificadores únicos para todas las entidades (Usuarios, Productos, Órdenes). 
El uso de identificadores secuenciales tradicionales (Integers autoincrementales: 1, 2, 3...) presenta problemas de seguridad (permiten enumeración de recursos y estimación del volumen de negocio) y dificultades en entornos distribuidos.
Por otro lado, los UUIDv4 (totalmente aleatorios) resuelven la seguridad, pero causan problemas de rendimiento en las bases de datos al fragmentar los índices debido a su falta de orden secuencial.

## Decisión
Se utilizará **UUIDv7** como Clave Primaria (Primary Key) estándar para todas las tablas del sistema.

Los IDs serán generados a nivel de aplicación (FastAPI/Python) antes de la inserción, utilizando librerías compatibles con el borrador del estándar IETF (ej: `uuid6` o `uuid-utils`).

## Justificación
Se eligió la versión 7 sobre la versión 4 o los Integers por las siguientes razones:

1.  **Ordenable por Tiempo (Time-sortable):** UUIDv7 incluye una marca de tiempo en sus primeros bits. Esto permite que los índices B-Tree de PostgreSQL mantengan un orden físico eficiente, evitando la fragmentación y la penalización de rendimiento en las inserciones (INSERT) que sufren los UUIDv4.
2.  **Seguridad:** Al igual que UUIDv4, son prácticamente imposibles de adivinar, evitando ataques de enumeración (ej: un atacante no puede probar `/users/5` y luego `/users/6`).
3.  **Generación Distribuida:** No se depende de la base de datos para generar el ID (como con `serial`), lo que facilita generar IDs en el código Python.

## Consecuencias

### Positivas
* **Rendimiento de Base de Datos:** Las inserciones masivas serán más rápidas que con UUIDv4.
* **Ordenamiento Implícito:** Se podra ordenar por la columna `id` y se obtendra el orden cronológico de creación.
* **Consistencia:** Todo el sistema usa el mismo formato de 128-bits.

### Negativas / Requisitos
* **Dependencia:** Python (en versiones < 3.13) no trae UUIDv7 nativo, por lo que se requiere instalar la dependencia externa `uuid6`.
* **Almacenamiento:** Un UUID ocupa 128 bits (16 bytes), que es más que un Integer (4 bytes) o BigInt (8 bytes), lo que aumenta ligeramente el tamaño de la BD y los índices, un costo aceptable por las ventajas obtenidas.