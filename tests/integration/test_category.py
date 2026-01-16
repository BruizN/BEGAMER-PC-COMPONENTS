import pytest

async def test_create_category_ok(
    admin_client
):
    payload = {
        "name": "tarjeta de Video",
        "code": "gpu"
    }

    response = await admin_client.post("/catalog/categories", json=payload)

    assert response.status_code == 201
    data = response.json()
    #Comprobar .title() y upper()
    assert data["name"] == payload["name"].title()
    assert data["code"] == payload["code"].upper()
    assert "category_id" in data


async def test_list_categories_ok(
    admin_client,
    category_factory
):
    await category_factory(name="Tarjeta de video", code="gpu")
    await category_factory(name="Fuente de alimentación", code="psu")

    response = await admin_client.get("/catalog/categories")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

async def test_update_categories_ok(
    admin_client,
    category_factory
):
    old_category = await category_factory(name="tarjeta devideo", code="gpu")
    
    payload = {"name": "tarjeta de video"}

    response = await admin_client.patch(
        f"/catalog/categories/{old_category.category_id}", 
        json=payload
        )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"].title()
    #Comprobar actualización parcial
    assert data["code"] == old_category.code.upper()
    assert data["category_id"] == str(old_category.category_id)

async def test_delete_categories_ok(
    admin_client,
    category_factory
):
    category = await category_factory(name="proce", code="prc")

    response = await admin_client.delete(
        f"/catalog/categories/{category.category_id}"
        )
    
    assert response.status_code == 204



async def test_deny_duplicated_category_creation(
    admin_client,
    category_factory
):
    await category_factory(name="Procesador", code="CPU")
    
    payload = {
        "name": "proceSADOR",
        "code": "cpu"
    }

    response = await admin_client.post("/catalog/categories", json=payload)
    #Comprobar duplicados independientemente de si los nombres esten capitalizados o no
    assert response.status_code == 409

async def test_deny_duplicated_category_mofication(
    admin_client,
    category_factory
):
    # Crea la categoría que se va a editar
    category = await category_factory(name="Procesador", code="CPU")
    
    # Crea la categoría "rival" (la que ya tiene el código ocupado)
    category2 = await category_factory(name="Tarjeta de video", code="GPU")
    
    payload = {
        "name": "proceSADOR",
        "code": "gpu"
    }

    response = await admin_client.patch(
        f"/catalog/categories/{category.category_id}", 
        json=payload
    )
    
    assert response.status_code == 409


#Comprobar denegación inmediata a usuarios clientes
@pytest.mark.parametrize("endpoint, method, status", [
    ("/catalog/categories", "post", 403),
    ("/catalog/categories", "get", 200),
    ("/catalog/categories/999", "patch", 403),
    ("/catalog/categories/999", "delete", 403),
])
async def test_category_permissions_for_client(
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
