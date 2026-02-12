import pytest
from datetime import datetime, timezone, timedelta

async def test_create_category_ok(
    admin_client
):
    payload = {
        "name": "Tarjeta de video",
        "code": "gpu"
    }

    response = await admin_client.post("/catalog/categories", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    #Comprobar upper()
    assert data["code"] == payload["code"].upper()
    assert data["is_active"]
    assert "created_at" in data
    assert "updated_at" in data
    assert "category_id" in data


#Comprobar paginación y que siendo admin se vean todas las categorías incluso las inactivas
async def test_list_categories_admin_ok(
    admin_client,
    category_factory
):
    await category_factory(name="Tarjeta de video", code="gpu", is_active=True)
    await category_factory(name="Fuente de alimentación", code="psu", is_active=True)
    await category_factory(name="Procesador", code="cpu", is_active=False)
    await category_factory(name="Memoria RAM", code="ram", is_active=True)
    await category_factory(name="Almacenamiento", code="sto", is_active=False)

    response = await admin_client.get("/catalog/categories?offset=2&limit=4")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


#Comprobar paginación y que siendo usuario solo se vean las categorías activas
async def test_list_categories_user_ok(
    user_client,
    category_factory
    ):
    await category_factory(name="Tarjeta de video", code="gpu", is_active=True)
    await category_factory(name="Fuente de alimentación", code="psu", is_active=True)
    await category_factory(name="Procesador", code="cpu", is_active=False)
    await category_factory(name="Memoria RAM", code="ram", is_active=True)
    await category_factory(name="Almacenamiento", code="sto", is_active=False)

    response = await user_client.get("/catalog/categories?offset=2&limit=4")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

#Comprobar denegación de acceso a categoría inactiva para usuarios sin rol de admin
async def test_deny_get_category_user_by_id(
    user_client,
    category_factory
):
    category = await category_factory(name="Tarjeta de video", code="gpu", is_active=False)
    response = await user_client.get(f"/catalog/categories/{category.category_id}")
    assert response.status_code == 404

#Comprobar acceso a categoría tanto activa como inactiva para usuarios con rol de admin
async def test_get_category_by_id_ok(
    admin_client,
    category_factory
):
    category = await category_factory(name="Tarjeta de video", code="gpu")
    response = await admin_client.get(f"/catalog/categories/{category.category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["category_id"] == str(category.category_id)
    assert data["name"] == category.name
    assert data["code"] == category.code.upper()
    assert data["is_active"] == category.is_active
    
    category2 = await category_factory(name="procesador", code="cpu", is_active=False)
    response = await admin_client.get(f"/catalog/categories/{category2.category_id}")
    assert response.status_code == 200


#Comprobar actualización parcial de una categoría y "soft delete"
async def test_update_categories_ok(
    admin_client,
    category_factory,
):
    past_date = datetime.now(timezone.utc) - timedelta(days=1)
    
    category = await category_factory(
        name="Tarjeta de video", 
        code="gpu", 
        created_at=past_date,
        updated_at=past_date
    )
    
    #Debido a como sqlalchemy actualiza los campos, guardamos el valor original en una variable aparte
    original_updated_at = category.updated_at
    original_id = str(category.category_id)

    payload = {"name": "Tarjeta De video", "is_active": False}

    response = await admin_client.patch(
        f"/catalog/categories/{original_id}", 
        json=payload
        )

    assert response.status_code == 200
    data = response.json()
    
    response_updated_at = datetime.fromisoformat(data["updated_at"])

    assert response_updated_at != original_updated_at
    assert response_updated_at > original_updated_at
    
    assert data["name"] == "Tarjeta De video"
    assert not data["is_active"]


#Comprobar eliminación de una categoría sin y con productos asociados
async def test_delete_categories(
    admin_client,
    category_factory,
    product_factory,
    brand_factory
):

    category = await category_factory(name="Procesador", code="cpu")

    response = await admin_client.delete(
        f"/catalog/categories/{category.category_id}"
        )
    
    assert response.status_code == 204

    #Comprobar que no se puede eliminar una categoría que tenga productos
    category2 = await category_factory(name="Tarjeta de video", code="gpu")
    brand = await brand_factory(name="Zotac", code="zot")
    await product_factory(
        name="Gaming GeForce RTX 4070 Twin Edge", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=category2, 
        brand=brand
        )

    response = await admin_client.delete(
        f"/catalog/categories/{category2.category_id}"
        )
    
    assert response.status_code == 409

async def test_deny_duplicated_category_creation(
    admin_client,
    category_factory
):
    await category_factory(name="Procesador", code="CPU")
    
    payload = {
        "name": "Procesador",
        "code": "cpu"
    }

    response = await admin_client.post("/catalog/categories", json=payload)
    assert response.status_code == 409

async def test_deny_duplicated_category_mofication(
    admin_client,
    category_factory
):
    # Crea la categoría que se va a editar
    category = await category_factory(name="Procesador", code="CPU")
    
    # Crea la categoría "rival" (la que ya tiene el código ocupado)
    await category_factory(name="Tarjeta de video", code="GPU")
    
    payload = {
        "name": "Procesador",
        "code": "gpu"
    }

    response = await admin_client.patch(
        f"/catalog/categories/{category.category_id}", 
        json=payload
    )
    
    assert response.status_code == 409


#Comprobar denegación inmediata a usuarios clientes
@pytest.mark.parametrize("endpoint, method", [
    ("/catalog/categories", "post"),
    ("/catalog/categories/999", "patch"),
    ("/catalog/categories/999", "delete"),
])
async def test_category_permissions_for_client(
    user_client,
    endpoint,
    method,
):

    request_func = getattr(user_client, method)
    
    response = await request_func(
        endpoint
    )
    assert response.status_code == 403
