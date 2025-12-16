---
name: Historia de Usuario
about: Describe this issue template's purpose here.
title: ''
labels: enhancement
assignees: ''

---

## 📖 Historia de Usuario (API): [Título Corto]

> **Como** [Cliente de la API / Frontend / Sistema externo]
> **Quiero** [Operación sobre la API: crear, listar, actualizar, etc.]
> **Para** [Objetivo o valor que se logra con esta operación]

---

## ✅ Criterios de Aceptación (API)

### 🟢 Escenarios de Éxito (Happy Path)
- [ ] **Escenario 1: [Nombre del flujo principal]**
  * **Dado** que envío una petición HTTP **[método]** a `[/ruta/del/endpoint]`
  * **Y** el cuerpo de la petición contiene:
    * `[campo1]` = [tipo / condición]
    * `[campo2]` = [tipo / condición]
  * **Cuando** el backend procesa la petición
  * **Entonces** debe responder con código **[200 / 201 / 204...]**
  * **Y** el cuerpo de la respuesta debe incluir:
    * `[campo_respuesta1]`
    * `[campo_respuesta2]`
  * **Y** el cambio debe reflejarse en la base de datos (registros creados/actualizados/eliminados).

### 🟠 Escenarios Alternativos y Errores (Edge Cases)
- [ ] **Escenario 2: Datos inválidos**
  * **Dado** que envío una petición HTTP con datos incompletos o inválidos
  * **Cuando** el backend valida la petición
  * **Entonces** debe responder con código **4xx (por ejemplo 400 o 422)**
  * **Y** el cuerpo de la respuesta debe incluir un mensaje de error descriptivo.

- [ ] **Escenario 3: Restricciones de negocio / base de datos**
  * **Dado** que intento realizar una operación que viola una regla (por ejemplo, SKU duplicado)
  * **Cuando** el backend intenta guardar los datos
  * **Entonces** debe responder con código **409 (Conflict)** u otro código definido
  * **Y** no debe modificar los datos existentes.

---

## 🔍 Notas de Pruebas (Opcional)
* Casos de prueba unitarios / de integración que validen:
  * Respuesta correcta del endpoint (status + body).
  * Escritura correcta en la base de datos (inserción / actualización / borrado).
  * Manejo de errores (validación, restricciones de unicidad, etc.).

---

> 🔧 Detalles más técnicos (modelo SQL, migraciones, estructura de tablas, ORMs, etc.) se documentan en el **SDD** o en la documentación técnica de la API.
