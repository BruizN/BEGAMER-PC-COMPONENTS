# BeGamer Components - Documentación de Arquitectura

## 🎯 Introducción
**BeGamer Components** es una plataforma de comercio electrónico especializada en la venta de hardware para PC. Este sistema gestiona el catálogo de productos (componentes), inventario, marcas y categorías, exponiendo una API RESTful para el consumo de clientes frontend y administradores.

Esta documentación describe la arquitectura de software del sistema utilizando los dos primeros niveles del modelo **C4 (Context y Containers)** y registra las Decisiones de Arquitectura (ADRs) clave que guían el desarrollo.

> **Nota de Estado:** Este proyecto se encuentra en desarrollo activo. Algunas integraciones descritas en el nivel de contexto (como Pasarela de Pagos o SII) representan el **diseño arquitectónico objetivo** y se encuentran en fase de planificación o simulación, no necesariamente implementadas en el código productivo actual.

## 🏗️ Estructura de la Documentación

En este sitio encontrarás:

1.  **Modelo C4 (Arquitectura):**
    * **Nivel 1 - Contexto del Sistema:** Visión general de los actores (Cliente, Admin) y cómo el sistema **interactuará** con servicios externos (Webpay, SII, Correo) en su versión final.
    * **Nivel 2 - Contenedores:** Desglose detallado de la arquitectura actual del Backend (API FastAPI), la Base de Datos y sus responsabilidades.
2.  **Modelo de Datos:** Diagramas Entidad-Relación (ER) de las tablas implementadas.
3.  **Decisiones de Arquitectura (ADRs):** Registro histórico del "por qué" de las decisiones técnicas (FastAPI, UUIDv7, PostgreSQL, etc.).

## 🚀 Tecnologías Clave
El sistema está construido sobre un stack moderno enfocado en rendimiento y seguridad:

* **Lenguaje:** Python 3.13
* **Framework Web:** FastAPI (Asíncrono)
* **Base de Datos:** PostgreSQL 15
* **Seguridad:** OAuth2 con JWT y Hashing Argon2
* **Infraestructura:** Docker & Docker Compose

## 👤 Autoría
Este proyecto es una iniciativa de desarrollo personal para aplicar estándares de ingeniería de software en un entorno simulado.

* **Autor:** Bruno Ruiz
* **Repositorio:** [GitHub](https://github.com/bruizn/begamer-pc-components)