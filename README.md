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

2.  **Configurar Variables de Entorno:**
    Crea un archivo `.env` en la raíz (puedes copiar el ejemplo abajo).
    > **Nota:** Para Docker, la URL de la base de datos debe usar el host `db`, no `localhost`.

    ```env
    # --- SEGURIDAD ---
    SECRET_KEY=7a9c8d2e1f3b4a5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60

    # --- BASE DE DATOS ---
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=Gamer_2026
    POSTGRES_DB=Begamer
    POSTGRES_DB_TEST=begamer_test

    # --- URLs DE CONEXIÓN (IMPORTANTE) ---
    # Para la App dentro de Docker:
    POSTGRES_URL=postgresql+asyncpg://admin:Gamer_2026@db:5432/Begamer
    
    # Para Tests (que corren en una red de prueba interna):
    TEST_DATABASE_URL=postgresql+asyncpg://admin:Gamer_2026@db_test:5432/begamer_test
    
    # Datos del Admin Inicial
    FIRST_SUPERUSER_EMAIL=begamer@gmail.com
    FIRST_SUPERUSER_PASSWORD=BegamerAdmin2026
    ```

3.  **Levantar el sistema:**
    ```bash
    docker-compose up --build -d
    ```
    *Espera unos segundos a que la base de datos esté saludable (healthy).*

4.  **Aplicar Migraciones y Crear Admin:**
    Ejecuta estos comandos *dentro* del contenedor backend (así evitas problemas de dependencias locales):

    ```bash
    # 1. Aplicar migraciones de base de datos
    docker-compose exec backend alembic upgrade head

    # 2. Crear superusuario inicial
    docker-compose exec backend python -m scripts.seed_admin
    ```

5.  **¡Listo! Accede a la API:**
    * 📄 **Swagger UI:** http://localhost:8000/docs
    * 📑 **Redoc:** http://localhost:8000/redoc

---

## 🧪 Testing

Para ejecutar la suite de pruebas (Integration Tests), usa el servicio de pruebas dedicado en Docker. Esto garantiza un entorno limpio y aislado.

```bash
docker-compose run --rm backend pytest

👤 Autor
* **Bruno Ruiz**
* Estudiante de Ingeniería en Informática (Duoc UC)
* Desarrollador Backend Autodidacta
* [GitHub Profile](https://github.com/BruizN)

Made with ❤️, lots of coffee and Python.