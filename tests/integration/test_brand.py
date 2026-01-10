import pytest

async def test_create_brand_ok(
    admin_client
):
    payload = {
        "name": "Brand1"
    }

    response =  await admin_client.post("/catalog/brand", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert "brand_id" in data

async def test_list_brands_ok(
    client,
    brand_factory
):
    await brand_factory(name="Brand1")
    await brand_factory(name="Brand2")

    response = await client.get("/catalog/brands")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

async def test_update_brand_ok(
    admin_client,
    brand_factory
):
    old_brand = await brand_factory(name="Brand1")

    payload = {
        "name": "Brand2"
    }

    response = await admin_client.put(
        f"/catalog/brand/{old_brand.brand_id}",
        json=payload
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["brand_id"] == str(old_brand.brand_id)

async def test_delete_brand_ok(
    admin_client,
    brand_factory
):
    brand = await brand_factory(name="Brand")

    response = await admin_client.delete(
        f"catalog/brand/{brand.brand_id}"
    )

    assert response.status_code == 204


async def test_deny_duplicated_brand(
    admin_client,
    brand_factory
):
    await brand_factory(name="Brand")

    payload = {
        "name": "Brand"
    }
    response = await admin_client.post("/catalog/brand", json=payload)
    assert response.status_code == 409

@pytest.mark.parametrize("endpoint, method, status", [
    ("/catalog/brand", "post", 403),
    ("/catalog/brands", "get", 200),
    ("/catalog/brand/999", "put", 403),
    ("/catalog/brand/999", "delete", 403),
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
