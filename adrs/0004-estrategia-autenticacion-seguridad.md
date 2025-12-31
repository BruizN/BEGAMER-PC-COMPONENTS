# 4. Estrategia de Autenticación y Seguridad

**Fecha:** 2025-12-23
**Estado:** Aceptado

## Contexto
El sistema requiere identificar a los administradores y clientes de forma segura. Se necesita un mecanismo para mantener la sesión del usuario entre peticiones de forma eficiente (stateless vs stateful) y una forma robusta de almacenar credenciales, ya que almacenar contraseñas en texto plano es inaceptable.

## Decisiones

### 1. Mecanismo de Sesión: JWT (JSON Web Tokens)
Se utilizará el esquema de autenticación **Bearer Token** con **JWT**.
* **Justificación:** Permite que la API sea completamente *stateless* (sin guardar sesiones en memoria o BD), lo que facilita el escalado horizontal.
* **Implementación:** FastAPI gestionará la seguridad de los endpoints mediante `HTTPBearer`, validando la firma del token en cada petición protegida.

### 2. Almacenamiento de Contraseñas: Hashing con Argon2
Se utilizará el algoritmo **Argon2** (vía librería `pwdlib`).
* **Justificación:** Argon2 es el ganador de la *Password Hashing Competition*. Es resistente a ataques de fuerza bruta por GPU/ASIC, siendo superior a estándares antiguos como SHA256 o MD5.

### 3. Librería de Criptografía: PyJWT
Se utilizará **PyJWT** para la generación (codificación) y validación (decodificación) de los tokens.

## Consecuencias
* **Responsabilidad del Cliente:** El frontend (o cliente API) debe encargarse de almacenar el token de forma segura y enviarlo en el header `Authorization` en cada petición.