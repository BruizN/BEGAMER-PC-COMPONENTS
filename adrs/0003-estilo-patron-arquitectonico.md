# Selección de Estilo(Macro arquitectónico) y Patron Arquitectónico(Micro arquitectónico)

* **Estado:** Aceptado
* **Fecha:** 2025-12-09

## Contexto
El sistema de e-commerce "BEGamer Components" requiere un estilo y patrones arquitectónicos que permitan una arquitectura limpia y mantenible. La arquitectura debe ser escalable y segura para proteger la información sensible de los usuarios.

## Estilos arquitectónicos considerados
* Monolitico
* Microservicios
* Monolitico modular

## Patrones arquitectónicos considerados
* Hexagonal Architecture
* Layered Architecture

## Decisión
Se seleccionará **Monolitico modular** junto a **Layered Architecture**.

## Justificación
El monolitico modular es una arquitectura donde toda la aplicación se despliega como una sola unidad (un solo artefacto/proceso), pero el código interno está estrictamente organizado en módulos de bajo acomplamiento basados en el dominio del negocio permitiendo que si se necesita escalar un modulo se puede convertir en un microservicio, gracias a que sigue siendo un monolito es mas simple para un equipo pequeño, a diferencia de microservicios que requieren mas experiencia y mas tiempo para implementar, pero seguimos conservando la ventaja de modulos con bajo acomplamiento. Ademas es optima para un equipo pequeño. Tambien debido al tamaño del equipo y del proyecto se escogera Layered Architecture ya que ofrece una forma simple de organizar el codigo. Se encontrara dentro de cada modulo(repository.py, router.py, service.py) y db.py como capa de infraestructura compartida.

### Consecuencias
* **Positivas:** El desarrollador cuenta con experiencia trabajando con esta arquitectura, ademas layered encaja muy bien con FastAPI.
* **Negativas:** Disciplina: Requiere madurez. Es muy fácil hacer trampa e importar código cruzado si no hay reglas de linter estrictas. 
* **Mitigacion:** La comunicación entre módulos se realizará mediante llamadas a métodos públicos (interfaces de servicio) y no mediante consultas directas a tablas de otros módulos.
