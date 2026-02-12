import pytest
from datetime import datetime, timezone, timedelta

async def test_create_brand_ok(
    admin_client
):
    payload = {
        "name": "Corsair",
        "code": "cor"
    }

    response = await admin_client.post("/catalog/brands", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    #Comprobar que se guarda en mayusculas
    assert data["code"] == payload["code"].upper()
    assert "brand_id" in data

#Comprobar paginación y que siendo admin se vean todas las marcas incluso las inactivas
async def test_list_brands_ok(
    admin_client,
    brand_factory
):
    await brand_factory(name="Corsair", code="cor", is_active=True)
    await brand_factory(name="Asus", code="asu", is_active=False)
    await brand_factory(name="Msi", code="msi", is_active=True)
    await brand_factory(name="Gigabyte", code="gig", is_active=False)
    await brand_factory(name="Razer", code="raz", is_active=True)

    response = await admin_client.get("/catalog/brands?offset=2&limit=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


#Comprobar paginación y que siendo usuario solo se vean las marcas activas
async def test_list_brands_user_ok(
    user_client,
    brand_factory
):
    await brand_factory(name="Corsair", code="cor", is_active=True)
    await brand_factory(name="Asus", code="asu", is_active=False)
    await brand_factory(name="Msi", code="msi", is_active=True)
    await brand_factory(name="Gigabyte", code="gig", is_active=False)
    await brand_factory(name="Razer", code="raz", is_active=True)

    response = await user_client.get("/catalog/brands?offset=2&limit=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

#Comprobar denegación de acceso a marca inactiva para usuarios sin rol de admin
async def test_deny_get_brand_user_by_id(
    user_client,
    brand_factory
):
    brand = await brand_factory(name="Asus", code="asu", is_active=False)
    response = await user_client.get(f"/catalog/brands/{brand.brand_id}")
    assert response.status_code == 404

#Comprobar acceso a marca tanto activa como inactiva para usuarios con rol de admin
async def test_get_brand_by_id_ok(
    admin_client,
    brand_factory
):
    brand = await brand_factory(name="Asus", code="asu")
    response = await admin_client.get(f"/catalog/brands/{brand.brand_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["brand_id"] == str(brand.brand_id)
    assert data["name"] == brand.name
    assert data["code"] == brand.code.upper()
    assert data["is_active"] == brand.is_active
    
    brand2 = await brand_factory(name="Msi", code="msi", is_active=False)
    response = await admin_client.get(f"/catalog/brands/{brand2.brand_id}")
    assert response.status_code == 200


#Comprobar actualización parcial de una marca y "soft delete"
async def test_update_brand_ok(
    admin_client,
    brand_factory
):
    past_date = datetime.now(timezone.utc) - timedelta(days=1)
    
    brand = await brand_factory(
        name="Asus", 
        code="asu", 
        created_at=past_date,
        updated_at=past_date
    )
    
    #Debido a como sqlalchemy actualiza los campos, guardamos el valor original en una variable aparte
    original_updated_at = brand.updated_at
    original_id = str(brand.brand_id)

    payload = {"name": "Asus", "is_active": False}

    response = await admin_client.patch(
        f"/catalog/brands/{original_id}", 
        json=payload
        )

    assert response.status_code == 200
    data = response.json()
    
    response_updated_at = datetime.fromisoformat(data["updated_at"])

    assert response_updated_at != original_updated_at
    assert response_updated_at > original_updated_at
    
    assert data["name"] == "Asus"
    assert not data["is_active"]

#Comprobar eliminación de una marca sin y con productos asociados
async def test_delete_brand(
    admin_client,
    category_factory,
    product_factory,
    brand_factory
):

    brand = await brand_factory(name="Asus", code="asu")

    response = await admin_client.delete(
        f"/catalog/brands/{brand.brand_id}"
        )
    
    assert response.status_code == 204

    #Comprobar que no se puede eliminar una marca que tenga productos
    brand2 = await brand_factory(name="Zotac", code="zot")
    category = await category_factory(name="Tarjeta de video", code="gpu")
    await product_factory(
        name="Gaming GeForce RTX 4070 Twin Edge", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=category, 
        brand=brand2
        )

    response = await admin_client.delete(
        f"/catalog/brands/{brand2.brand_id}"
        )
    
    assert response.status_code == 409



async def test_deny_duplicated_brand_creation(
    admin_client,
    brand_factory
):
    await brand_factory(name="Asus", code="ASU")
    
    payload = {
        "name": "Asus",
        "code": "asu"
    }

    response = await admin_client.post("/catalog/brands", json=payload)
    #Comprobar duplicados independientemente de si los nombres esten capitalizados o no
    assert response.status_code == 409

async def test_deny_duplicated_brand_mofication(
    admin_client,
    brand_factory
):
    # Crea la categoría que se va a editar
    brand = await brand_factory(name="Asus", code="asu")
    
    # Crea la categoría "rival" (la que ya tiene el código ocupado)
    await brand_factory(name="Corsair", code="cor")
    
    payload = {
        "name": "Corsair",
        "code": "cor"
    }

    response = await admin_client.patch(
        f"/catalog/brands/{brand.brand_id}", 
        json=payload
    )
    
    assert response.status_code == 409


#Comprobar denegación inmediata a usuarios clientes
@pytest.mark.parametrize("endpoint, method", [
    ("/catalog/brands", "post"),
    ("/catalog/brands/999", "patch"),
    ("/catalog/brands/999", "delete"),
])
async def test_brand_permissions_for_client(
    user_client,
    endpoint,
    method,
):

    request_func = getattr(user_client, method)
    
    response = await request_func(
        endpoint
    )
    assert response.status_code == 403
