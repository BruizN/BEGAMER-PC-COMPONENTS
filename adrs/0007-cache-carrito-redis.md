# 6. Gestión de carrito con Redis y TTL

**Fecha:** 2026-03-15

## Contexto y Problema
El e-commerce requiere almacenar temporalmente el contenido del carrito de los usuarios 
almacenar temporalmente el contenido del carrito en PostgreSQL podria hacer que las escrituras y lecturas
sean considerablemente lentas ademas de que se necesitaria configurar un tiempo de expiracion y una estructura de tabla

## Opciones Consideradas
* **Redis** Excelente opcion para este tipo de escenarios, ofrece lectura y escritura de datos veloces.

## Decisión
Se utilizará **Redis** para el almacenamiento temporal de carritos de usuario.

## Justificación
1. **Estructura de datos flexible:** En redis se pueden usar Hashes para representar el carrito, donde la clave puede ser el token o un header de usuario y los campos son los productos con sus cantidades, esto permite actualizaciones atomicas sencillas.
2. **Velocidad de escritura/lectura:** Debido a ser una base de datos en memoria, la velocidad de escritura y lectura ocurre en un tiempo casi impercetible,para un carrito donde un usuario 
puede agregar y quitar items del carrito de forma constante esto es una mejora significativa.
3. **TTL:** Redis permite asignar un TTL a cada clave, permitiendo configurar que el carrito expire automaticamente en x tiempo.