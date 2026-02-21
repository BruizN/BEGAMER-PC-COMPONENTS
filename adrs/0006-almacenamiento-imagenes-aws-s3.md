# 6. Almacenamiento de Archivos Multimedia: AWS S3 y Boto3

**Fecha:** 2026-02-21
**Estado:** Aceptado

## Contexto y Problema
El e-commerce requiere gestionar y servir imágenes de los componentes de hardware (productos). 
Almacenar estos archivos binarios pesados directamente en la base de datos PostgreSQL (como `bytea`) degradaría severamente el rendimiento y aumentaría los costos de la base de datos. Por otro lado, almacenar los archivos en el disco local del servidor rompería el principio *stateless* de la API, impidiendo el escalado horizontal en el futuro (si un servidor cae, las imágenes guardadas localmente se perderían).

## Opciones Consideradas
* **Almacenamiento en Disco Local:** Rechazado por romper la arquitectura *stateless*.
* **Azure Blob Storage / Google Cloud Storage:** Opciones empresariales válidas.
* **AWS S3 (Amazon Simple Storage Service):** Solución de almacenamiento de objetos líder en el mercado.

## Decisión
Se utilizará **AWS S3** para el almacenamiento de todas las imágenes estáticas del sistema, interactuando con el servicio a través del SDK oficial de Python, **`boto3`**.

## Justificación
1. **Alineación con el Estándar de la Industria:** AWS es el proveedor de nube con mayor adopción a nivel empresarial.
2. **Eficiencia de Costos (Capa Gratuita):** El *Free Tier* de AWS ofrece 5 GB de almacenamiento estándar y 20,000 peticiones GET mensuales durante 12 meses, lo cual excede holgadamente las necesidades de un entorno de pruebas y exhibición académica.
3. **Desacoplamiento:** Delegar la carga de archivos a un servicio de objetos externo (Object Storage) mantiene la API de FastAPI ligera.

## Consecuencias

### Positivas
* **Fiabilidad:** AWS S3 es un servicio altamente confiable y escalable.
* **Valor Profesional:** Incorpora el manejo de credenciales cloud, políticas IAM y SDKs empresariales al stack tecnológico del proyecto.

### Negativas / Riesgos
* **Gestión de Secretos:** Requiere disciplina estricta para no exponer las credenciales (`AWS_ACCESS_KEY_ID` y `AWS_SECRET_ACCESS_KEY`) en el control de versiones (GitHub). Se deberá utilizar obligatoriamente un archivo `.env`.
* **Curva de Integración:** Requiere aprender la sintaxis de `boto3`.