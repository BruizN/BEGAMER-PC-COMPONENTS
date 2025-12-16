# 1. Selección de Stack Tecnológico para Backend

**Fecha:** 2025-12-09
**Estado:** Aceptado

## Contexto
El proyecto "BEGamer Components" requiere el desarrollo de una API REST eficiente y documentada para gestionar el inventario y las ventas. El equipo de desarrollo (unipersonal) cuenta con un tiempo limitado para la implementación y requiere herramientas que permitan un desarrollo ágil.

Limitaciones:
* El desarrollador tiene experiencia previa y dominio de Python.
* Se requiere validación de datos robusta para evitar errores en las órdenes de compra.

## Decisión
Se utilizará el lenguaje **Python** junto con el framework **FastAPI**.

Se descartan otros lenguajes (como Java o C#) debido a la curva de aprendizaje que implicarían, lo cual pondría en riesgo los plazos de entrega del proyecto.

## Consecuencias

### Positivas
* **Velocidad de Desarrollo:** Al aprovechar el conocimiento existente en Python, se reduce el tiempo de configuración y codificación ("Time to market").
* **Documentación Automática:** FastAPI genera automáticamente documentación interactiva (Swagger UI / OpenAPI), lo cual es vital para probar los endpoints sin construir un frontend inmediatamente.
* **Validación de Datos:** El uso de Pydantic (integrado en FastAPI) asegura que los datos de entrada (precios, stock) sean correctos antes de procesarlos.
* **Asincronismo:** Permite manejar múltiples solicitudes concurrentes de manera eficiente.

### Negativas / Riesgos
* **Curva de Aprendizaje en Patrones Avanzados:** Aunque se conoce el framework, la implementación de patrones de arquitectura limpia y seguridad avanzada requerirá investigación adicional durante el desarrollo.