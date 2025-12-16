# Selección de Motor de Base de Datos Principal

* **Estado:** Aceptado
* **Fecha:** 2025-12-09

## Contexto
El sistema de e-commerce "BEGamer Components" requiere almacenar información de productos, usuarios, inventario y órdenes de compra. La integridad de los datos en las órdenes y el inventario es crítica (no podemos vender stock que no existe).


## Opciones Consideradas
* PostgreSQL
* SQLite

## Decisión
Se seleccionará **PostgreSQL**.

## Justificación
Al ser un e-commerce, la relación entre tablas (Usuario -> Orden -> Detalle -> Producto) es fuerte. Se necesitan transacciones ACID para asegurar que al comprar, se descuente el stock inmediatamente. PostgreSQL ofrece esto y además tiene buen soporte para JSON si se necesita guardar especificaciones técnicas flexibles de los PC.

### Consecuencias
* **Positivas:** Integridad referencial fuerte. Stack tecnológico alineado con el mercado laboral enterprise, desarrollador con experiencia en PostgreSQL.
* **Negativas:** Requiere definir esquemas (migrations) antes de programar, y una configuracion adicional para la base de datos PostgreSQL.
* **Mitigacion:** Configurar la base de datos mediante docker y diagramar la base de datos con diagrama ER.