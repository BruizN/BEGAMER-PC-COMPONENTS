import pytest

async def test_create_brand_ok(
    admin_client
):
    payload = {
        "name": "corsair",
        "code": "cors"
    }

    response = await admin_client.post("/catalog/brand", json=payload)

    assert response.status_code == 201
    data = response.json()
    #Comprobar .title() y upper()
    assert data["name"] == payload["name"].title()
    assert data["code"] == payload["code"].upper()
    assert "brand_id" in data


async def test_list_brands_ok(
    admin_client,
    brand_factory
):
    await brand_factory(name="corsair", code="cor")
    await brand_factory(name="asus", code="asu")

    response = await admin_client.get("/catalog/brands")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

async def test_update_brand_ok(
    admin_client,
    brand_factory
):
    old_brand = await brand_factory(name="asssus", code="asu")
    
    payload = {"name": "asus"}

    response = await admin_client.patch(
        f"/catalog/brand/{old_brand.brand_id}", 
        json=payload
        )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"].title()
    #Comprobar actualización parcial
    assert data["code"] == old_brand.code.upper()
    assert data["brand_id"] == str(old_brand.brand_id)

async def test_delete_brand_ok(
    admin_client,
    brand_factory
):
    brand = await brand_factory(name="asus", code="asu")

    response = await admin_client.delete(
        f"/catalog/brand/{brand.brand_id}"
        )
    
    assert response.status_code == 204



async def test_deny_duplicated_brand_creation(
    admin_client,
    brand_factory
):
    await brand_factory(name="AsUs", code="ASU")
    
    payload = {
        "name": "asus",
        "code": "asu"
    }

    response = await admin_client.post("/catalog/brand", json=payload)
    #Comprobar duplicados independientemente de si los nombres esten capitalizados o no
    assert response.status_code == 409

async def test_deny_duplicated_brand_mofication(
    admin_client,
    brand_factory
):
    # Crea la categoría que se va a editar
    brand = await brand_factory(name="asus", code="asu")
    
    # Crea la categoría "rival" (la que ya tiene el código ocupado)
    await brand_factory(name="corsair", code="cor")
    
    payload = {
        "name": "corsair",
        "code": "cor"
    }

    response = await admin_client.patch(
        f"/catalog/brand/{brand.brand_id}", 
        json=payload
    )
    
    assert response.status_code == 409


#Comprobar denegación inmediata a usuarios clientes
@pytest.mark.parametrize("endpoint, method, status", [
    ("/catalog/brand", "post", 403),
    ("/catalog/brands", "get", 200),
    ("/catalog/brand/999", "patch", 403),
    ("/catalog/brand/999", "delete", 403),
])
async def test_brand_permissions_for_client(
    user_client,
    endpoint,
    method,
    status,
):

    request_func = getattr(user_client, method)
    
    response = await request_func(
        endpoint
    )
    assert response.status_code == status
