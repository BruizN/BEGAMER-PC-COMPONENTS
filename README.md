# 🎮 BeGamer Components - Backend API

![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-009688.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)
![CI Status](https://github.com/bruizn/begamer-pc-components/actions/workflows/ci.yml/badge.svg)

> **Nota:** Este es un proyecto personal desarrollado como iniciativa propia durante mis vacaciones de verano. Todo el ciclo de vida (investigación, planificación, arquitectura y desarrollo) ha sido ejecutado de forma autónoma con el objetivo de dominar estándares de la industria y simular un entorno profesional. **Actualmente se encuentra en desarrollo activo.**

## 💡 Sobre el Proyecto

**BeGamer Components** es una API RESTful asíncrona para una plataforma de e-commerce de hardware de PC.

El objetivo principal de este proyecto no es solo "que funcione", sino demostrar **cómo se construye software mantenible, escalable y seguro**. Se ha implementado siguiendo flujos de trabajo profesionales como Kanban, CI/CD y revisiones de código estrictas.

### ✨ Características Principales (Hasta ahora)
* **Gestión de Catálogo:** CRUD completo para Productos, Marcas y Categorías con soporte para *Soft Delete* y Slugs automáticos.
* **Seguridad Robusta:** Autenticación JWT (Stateless) y hashing de contraseñas con **Argon2**.
* **Identificadores Modernos:** Implementación de **UUIDv7** para claves primarias (Time-sortable), optimizando la indexación en base de datos frente a UUIDv4.
* **Roles y Permisos:** Sistema RBAC (Role-Based Access Control) diferenciando entre Clientes y Administradores.
* **Arquitectura Limpia:** Diseño modular con separación de responsabilidades (Router → Service → Repository).

## 🔮 Roadmap & Próximos Pasos

El proyecto está en constante evolución. Actualmente, el foco de desarrollo está puesto en:

* 💳 **Pasarela de Pagos (Sandbox):**
    * Integración con **Webpay (Transbank)** en ambiente de pruebas.
    * Simulación completa del flujo de compra: *Inicio de transacción -> Pago en pasarela -> Validación de retorno -> Generación de Orden*.

* 🖼️ **Gestión de Imágenes:**
    * Sistema robusto para la subida, validación y optimización de imágenes de productos.
    * Estrategia de almacenamiento eficiente para activos estáticos.

---

## 🛠️ Stack Tecnológico

### Backend Core
* **Lenguaje:** Python 3.13
* **Framework:** FastAPI (Asíncrono)
* **ORM:** SQLModel (SQLAlchemy + Pydantic)
* **Base de Datos:** PostgreSQL 15

### Ingeniería & DevOps
* **Contenerización:** Docker & Docker Compose
* **Migraciones:** Alembic
* **Testing:** Pytest (Tests de Integración y Unitarios)
* **CI/CD:** GitHub Actions (Linting, Testing y Generación de Documentación)

---

## 🏗️ Arquitectura y Documentación

Este proyecto documenta sus decisiones arquitectónicas explícitamente.

### 1. C4 Model & Diagramas
Utilizo **Structurizr** para definir la arquitectura como código.
* [Ver Diagrama de Contexto y Contenedores](https://bruizn.github.io/BEGAMER-PC-COMPONENTS/master/)

### 2. Decisiones de Arquitectura (ADRs)
Cada decisión técnica importante está registrada en la carpeta `/adrs` siguiendo el formato *Architecture Decision Records*:
* [ADR-001: Selección de Stack (FastAPI)](adrs/0001-usar-python-fastapi.md)
* [ADR-003: Arquitectura Modular Monolítica](adrs/0003-estilo-patron-arquitectonico.md)
* [ADR-005: Estrategia de IDs (UUIDv7)](adrs/0005-estrategia-identificadores-uuidv7.md)

### 3. Modelo de Datos
El diseño de base de datos incluye índices optimizados y relaciones con integridad referencial.
* [Ver Diagrama Entidad-Relación (ER)](docs/er.md)

---

## 🚀 Metodología de Trabajo

Para simular un entorno real, el desarrollo sigue estas reglas:

* **Kanban y Transparencia:** Gestión de tareas mediante **GitHub Projects**.
  > 🔗 [Ver Tablero de Proyecto](https://github.com/users/BruizN/projects/4/views/1)  
  > *Aquí puedes visualizar en tiempo real qué se está trabajando, qué está en revisión y qué se planea*
* **Branch Protection:** La rama `main` está protegida.
* **Pull Requests:** Ningún código entra a producción sin pasar por una PR que cumpla:
    1.  Pasar el Pipeline de CI (Tests + Linter `Ruff`).
    2.  Cumplir con la plantilla de descripción de cambios.
---

## ⚡ Instalación y Ejecución

El proyecto está dockerizado para facilitar el despliegue.

### Prerrequisitos
* Docker y Docker Compose instalados.

### Pasos Rápidos

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/bruizn/begamer-pc-components.git](https://github.com/bruizn/begamer-pc-components.git)
    cd begamer-pc-components
    ```

2.  **Configuración de Almacenamiento (AWS S3) y configurar Variables de Entorno:**
Este proyecto utiliza **Amazon S3** para el almacenamiento de archivos e imágenes. Para el entorno de desarrollo, se asume el uso de una cuenta con el **Free Tier** activo.

#### Requisitos en AWS
1. **IAM User**: Crea un usuario en la consola de IAM con acceso programático.
2. **Políticas**: Asigna la política `AmazonS3FullAccess` a dicho usuario.
3. **Bucket**: Crea un bucket en S3 y asegúrate de que la región coincida con la configurada en el código.

Finalmente crea un archivo `.env` en la raíz (Revisa el .env.example).
    > **Nota:** Para Docker, la URL de la base de datos debe usar el host `db`, no `localhost`.

    

5.  **Levantar el sistema:**
    ```bash
    docker-compose up --build -d
    ```
    *Espera unos segundos a que la base de datos esté saludable (healthy).*

6.  **Aplicar Migraciones y Crear Admin:**
    Ejecuta estos comandos *dentro* del contenedor backend (así evitas problemas de dependencias locales):

    ```bash
    # 1. Aplicar migraciones de base de datos
    docker-compose exec backend alembic upgrade head

    # 2. Crear superusuario inicial
    docker-compose exec backend python -m scripts.seed_admin
    ```

7.  **Listo. Accede a la API:**
    * 📄 **Swagger UI:** http://localhost:8000/docs
    * 📑 **Redoc:** http://localhost:8000/redoc

---

## 🧪 Testing

Para ejecutar la suite de pruebas (Integration Tests), usa el servicio de pruebas dedicado en Docker. Esto garantiza un entorno limpio y aislado.

```bash
docker-compose run --rm backend pytest
```

👤 Autor
* **Bruno Ruiz**
* Estudiante de Ingeniería en Informática (Duoc UC)
* Desarrollador Backend Autodidacta
* [GitHub Profile](https://github.com/BruizN)
