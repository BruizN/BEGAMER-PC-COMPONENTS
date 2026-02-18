import pytest
from datetime import datetime, timezone, timedelta
#Comprobar creación de variantes y sku generado
async def test_create_variant_ok(
    admin_client,
    product_factory,
    brand_factory,
    category_factory
):
    brand = await brand_factory(name="zotac", code="zot")
    cat = await category_factory(name="tarjeta de video", code="gpu")
    product = await product_factory(name="Gaming GeForce RTX 4070 Twin Edge", category=cat, brand=brand)

    payload = {
        "price": "200000",
        "stock": "10",
        "attributes": "White Edition, 8GB VRAM"
    }

    response = await admin_client.post(f"/catalog/products/{product.product_id}/variants", json=payload)

    assert response.status_code == 201
    expected_sku = "GPU-ZOT-GAMING-GEFORCE-RTX-4070-TWIN-EDGE-WHITE-EDITION-8GB-VRAM"
    data = response.json()

    assert data["sku"] == expected_sku

#Comprobar paginación y que siendo admin se vean todas las variantes de un producto
async def test_list_variants_ok(
    admin_client,
    product_factory,
    variant_factory
):
    prod = await product_factory(name="Gaming GeForce RTX 4070 Twin Edge")
    await variant_factory(attributes = "White Edition, 8GB VRAM", product=prod)
    await variant_factory(attributes = "Black Edition, 8GB VRAM", product=prod, is_active=False)
    await variant_factory(attributes = "White Edition, 12GB VRAM", product=prod, is_active=False)
    response = await admin_client.get(f"/catalog/products/{prod.product_id}/variants?offset=0&limit=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

#Comprobar paginación y que siendo usuario común solo se vean las variantes de un producto acticas
async def test_user_list_variants_ok(
    user_client,
    product_factory,
    variant_factory
):
    prod = await product_factory(name="Gaming GeForce RTX 4070 Twin Edge")
    await variant_factory(attributes = "White Edition, 8GB VRAM", product=prod)
    await variant_factory(attributes = "Black Edition, 8GB VRAM", product=prod, is_active=False)
    await variant_factory(attributes = "White Edition, 12GB VRAM", product=prod, is_active=False)
    response = await user_client.get(f"/catalog/products/{prod.product_id}/variants?offset=0&limit=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


#Comprobar filtro por is active con admin
async def test_admin_list_variants_by_is_active(
    admin_client,
    product_factory,
    variant_factory
):
    prod = await product_factory(name="Gaming GeForce RTX 4070 Twin Edge")
    await variant_factory(attributes = "White Edition, 8GB VRAM", product=prod)
    await variant_factory(attributes = "Black Edition, 8GB VRAM", product=prod, is_active=False)
    await variant_factory(attributes = "White Edition, 12GB VRAM", product=prod, is_active=False)
    response = await admin_client.get(f"/catalog/products/{prod.product_id}/variants?offset=0&limit=2&is_active=false")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

#Comprobar filtro por is active con usuario común (no puede ver variantes inactivas aunque se fuerze el filtro)
async def test_user_list_variants_by_is_active(
    user_client,
    product_factory,
    variant_factory
):
    prod = await product_factory(name="Gaming GeForce RTX 4070 Twin Edge")
    await variant_factory(attributes = "White Edition, 8GB VRAM", product=prod)
    await variant_factory(attributes = "Black Edition, 8GB VRAM", product=prod, is_active=False)
    await variant_factory(attributes = "White Edition, 12GB VRAM", product=prod, is_active=False)
    response = await user_client.get(f"/catalog/products/{prod.product_id}/variants?offset=0&limit=2&is_active=false")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

#Comprobar denegación de acceso a producto inactivo para usuarios sin rol de admin
async def test_user_get_variant_by_id_denied(
    user_client,
    variant_factory
):
    variant = await variant_factory(attributes = "White Edition, 8GB VRAM", is_active=False)
    response = await user_client.get(f"/catalog/variants/{variant.variant_id}")
    assert response.status_code == 404

#Comprobar acceso a producto tanto activo como inactivo para usuarios con rol de admin
async def test_admin_get_variant_by_id(
    admin_client,
    product_factory,
    variant_factory
):
    prod = await product_factory(name="Gaming GeForce RTX 4070 Twin Edge")
    variant = await variant_factory(
        attributes = "White Edition, 8GB VRAM", is_active=True, price=200000, stock=10, product=prod
        )
    response = await admin_client.get(f"/catalog/variants/{variant.variant_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["attributes"] == variant.attributes
    assert data["is_active"] == variant.is_active
    assert data["price"] == str(variant.price)
    assert data["stock"] == variant.stock

    variant2 = await variant_factory(attributes = "Black Edition, 8GB VRAM", is_active=False, product=prod)
    response = await admin_client.get(f"/catalog/variants/{variant2.variant_id}")
    assert response.status_code == 200

#Comprobar actualización parcial de una variante, soft delete y sku
async def test_update_variant_ok(
    admin_client,
    variant_factory,
    product_factory,
    brand_factory,
    category_factory
):
    past_date = datetime.now(timezone.utc) - timedelta(days=1)
    brand = await brand_factory(name="zotac", code="zot")
    cat = await category_factory(name="tarjeta de video", code="gpu")
    prod = await product_factory(name="Gaming GeForce RTX 4070 Twin Edge", category=cat, brand=brand)
    
    variant = await variant_factory(
        attributes = "White Edition, 8GB VRAM", is_active=True, price=200000, stock=10, product=prod,
        created_at=past_date,
        updated_at=past_date
        )
    
    #Debido a como sqlalchemy actualiza los campos, guardamos el valor original en una variable aparte
    original_sku = variant.sku
    original_updated_at = variant.updated_at
    original_id = str(variant.variant_id)

    payload = {"attributes": "Black Edition, 12GB VRAM", "is_active": False}

    response = await admin_client.patch(
        f"/catalog/variants/{original_id}", 
        json=payload
        )

    assert response.status_code == 200
    assert response.json()["sku"] != original_sku
    assert response.json()["sku"] == "GPU-ZOT-GAMING-GEFORCE-RTX-4070-TWIN-EDGE-BLACK-EDITION-12GB-VRAM"
    data = response.json()
    
    response_updated_at = datetime.fromisoformat(data["updated_at"])

    assert response_updated_at != original_updated_at
    assert response_updated_at > original_updated_at
    
    assert data["attributes"] == "Black Edition, 12GB VRAM"
    assert not data["is_active"]

#Comprobar eliminación de una variante sin y con ordenes
async def test_delete_variant(
    admin_client,
    variant_factory
):
    variant = await variant_factory(
        attributes = "White Edition, 8GB VRAM"
        )

    response = await admin_client.delete(
        f"/catalog/variants/{variant.variant_id}"
        )
    
    assert response.status_code == 204

    #TODO: Comprobar que no se puede eliminar una variante que tenga ordenes
    
    # assert response.status_code == 409


#Comprobar que no se puede crear una variante con el mismo sku
async def test_deny_duplicated_variant_sku_creation(
    admin_client,
    variant_factory,
    product_factory
):
    prod = await product_factory(name="Gaming GeForce RTX 4070 Twin Edge")
    await variant_factory(attributes = "White Edition, 8GB VRAM", product=prod)

    payload = {
        "attributes": "White Edition, 8GB VRAM",
        "stock": 10,
        "price": 200000
    }

    response = await admin_client.post(f"/catalog/products/{prod.product_id}/variants", json=payload)
    assert response.status_code == 409

#Comprobar denegación inmediata a usuarios clientes
@pytest.mark.parametrize("endpoint, method", [
    ("/catalog/products/999/variants", "post"),
    ("/catalog/variants/999", "patch"),
    ("/catalog/variants/999", "delete"),
])
async def test_product_permissions_for_client(
    user_client,
    endpoint,
    method,
):

    request_func = getattr(user_client, method)
    
    response = await request_func(
        endpoint
    )
    assert response.status_code == 403
