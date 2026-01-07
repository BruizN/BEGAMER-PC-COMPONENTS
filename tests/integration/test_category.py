import pytest

async def test_create_category_ok(
    admin_client
):
    payload = {
        "name": "Procesador"
    }

    response = await admin_client.post("/catalog/categories", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert "category_id" in data


async def test_list_categories_ok(
    admin_client,
    category_factory
):
    await category_factory(name="Tarjeta de video")
    await category_factory(name="Fuente de alimentación")

    response = await admin_client.get("/catalog/categories")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

async def test_update_categories_ok(
    admin_client,
    category_factory
):
    old_category = await category_factory(name="Old Name")
    
    payload = {"name": "New Updated Name"}

    response = await admin_client.put(
        f"/catalog/categories/{old_category.category_id}", 
        json=payload
        )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["category_id"] == str(old_category.category_id)

async def test_delete_categories_ok(
    admin_client,
    category_factory
):
    category = await category_factory(name="Wrong category")

    response = await admin_client.delete(
        f"/catalog/categories/{category.category_id}"
        )
    
    assert response.status_code == 204



async def test_deny_duplicated_category(
    admin_client,
    category_factory
):
    await category_factory(name="Same category")
    
    payload = {
        "name": "Same category"
    }

    response = await admin_client.post("/catalog/categories", json=payload)
    assert response.status_code == 409



@pytest.mark.parametrize("endpoint, method, status", [
    ("/catalog/categories", "post", 403),
    ("/catalog/categories", "get", 200),
    ("/catalog/categories/999", "put", 403),
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
