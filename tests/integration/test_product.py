import pytest
from datetime import datetime, timezone, timedelta
from slugify import slugify

#Comprobar creación de producto y slug generado
async def test_create_product_ok(
    admin_client,
    brand_factory,
    category_factory
):
    brand = await brand_factory(name="corsair", code="cor")
    category = await category_factory(name="tarjeta de video", code="gpu")

    payload = {
        "name": "Gaming GeForce RTX 4070 Twin Edge",
        "description": "lorem ipsum dolor sit amet consectetur adipiscing elit",
        "brand_id": str(brand.brand_id),
        "category_id": str(category.category_id)
    }

    nombre_producto = payload["name"]
    nombre_marca = brand.name

    if nombre_producto.lower().startswith(nombre_marca.lower()):
        slug_text = f"{category.code} {nombre_producto}" 
    else:
        slug_text = f"{category.code} {nombre_marca} {nombre_producto}"

    generated_slug = slugify(slug_text)
    payload["slug"] = generated_slug

    response = await admin_client.post("/catalog/products", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["slug"] == generated_slug
    assert "product_id" in data

#Comprobar paginación y que siendo admin se vean todos los productos activos e inactivos
async def test_list_products_ok(
    admin_client,
    brand_factory,
    category_factory,
    product_factory
):
    brand1 = await brand_factory(name="zotac", code="zot")
    cat1 = await category_factory(name="tarjeta de video", code="gpu")
    await product_factory(
        name="Gaming GeForce RTX 4070 Twin Edge", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=cat1, 
        brand=brand1,
        is_active=False
        )

    brand2 = await brand_factory(name="intel", code="int")
    cat2 = await category_factory(name="Procesador", code="cpu")
    await product_factory(
        name="Core i9-14900K", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=cat2, 
        brand=brand2,
        is_active=False
        )

    brand3 = await brand_factory(name="helios", code="hel")
    cat3 = await category_factory(name="fuente de poder", code="psu")
    await product_factory(
        name="Helios 1000W 80 Plus Gold", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=cat3, 
        brand=brand3
        )

    response = await admin_client.get("/catalog/products?offset=0&limit=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


#Comprobar paginación y que siendo usuario común solo se vean los productos activos
async def test_list_products_user_ok(
    user_client,
    category_factory,
    brand_factory,
    product_factory
):
    brand1 = await brand_factory(name="zotac", code="zot")
    cat1 = await category_factory(name="tarjeta de video", code="gpu")
    await product_factory(
        name="Gaming GeForce RTX 4070 Twin Edge", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=cat1, 
        brand=brand1,
        is_active=False
        )

    brand2 = await brand_factory(name="intel", code="int")
    cat2 = await category_factory(name="Procesador", code="cpu")
    await product_factory(
        name="Core i9-14900K", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=cat2, 
        brand=brand2,
        is_active=False
        )

    brand3 = await brand_factory(name="helios", code="hel")
    cat3 = await category_factory(name="fuente de poder", code="psu")
    await product_factory(
        name="Helios 1000W 80 Plus Gold", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=cat3, 
        brand=brand3
        )

    response = await user_client.get("/catalog/products?offset=0&limit=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

#Comprobar denegación de acceso a producto inactivo para usuarios sin rol de admin
async def test_user_get_product_by_id_denied(
    user_client,
    brand_factory,
    category_factory,
    product_factory
):
    brand = await brand_factory(name="asus", code="asu")
    cat = await category_factory(name="tarjeta de video", code="gpu")
    prod = await product_factory(
        name="Gaming GeForce RTX 4070 Twin Edge", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=cat, brand=brand, 
        is_active=False
        )
    response = await user_client.get(f"/catalog/products/{prod.product_id}")
    assert response.status_code == 404

#Comprobar acceso a producto tanto activo como inactivo para usuarios con rol de admin
async def test_admin_get_product_by_id(
    admin_client,
    brand_factory,
    category_factory,
    product_factory
):
    brand = await brand_factory(name="asus", code="asu")
    cat = await category_factory(name="tarjeta de video", code="gpu")
    prod = await product_factory(
        name="Gaming GeForce RTX 4070 Twin Edge", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=cat, brand=brand
        )
    response = await admin_client.get(f"/catalog/products/{prod.product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == str(prod.product_id)
    assert data["name"] == prod.name
    assert data["description"] == prod.description
    assert data["category_id"] == str(prod.category_id)
    assert data["brand_id"] == str(prod.brand_id)
    assert data["is_active"] == prod.is_active
    

    assert response.status_code == 200

    brand2 = await brand_factory(name="intel", code="int")
    cat2 = await category_factory(name="procesador", code="cpu")
    prod2 = await product_factory(
        name="Core i9-14900K", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=cat2, brand=brand2, is_active=False
        )
    response = await admin_client.get(f"/catalog/products/{prod2.product_id}")
    assert response.status_code == 200


#Comprobar actualización parcial de un producto y soft delete
async def test_update_product_ok(
    admin_client,
    brand_factory,
    category_factory,
    product_factory
):
    past_date = datetime.now(timezone.utc) - timedelta(days=1)
    brand = await brand_factory(name="intel", code="int")
    brand2 = await brand_factory(name="amd", code="amd")
    cat = await category_factory(name="procesador", code="cpu")
    
    product = await product_factory(
        name="Core i9-14900K", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=cat, brand=brand,
        created_at=past_date,
        updated_at=past_date
    )
    
    #Debido a como sqlalchemy actualiza los campos, guardamos el valor original en una variable aparte
    original_updated_at = product.updated_at
    original_id = str(product.product_id)

    payload = {"name": "ryzen 9 7950x", "brand_id": str(brand2.brand_id), "is_active": False}

    response = await admin_client.patch(
        f"/catalog/products/{original_id}", 
        json=payload
        )

    assert response.status_code == 200
    data = response.json()
    
    response_updated_at = datetime.fromisoformat(data["updated_at"])

    assert response_updated_at != original_updated_at
    assert response_updated_at > original_updated_at
    
    assert data["name"] == "ryzen 9 7950x"
    assert data["brand_id"] == str(brand2.brand_id)
    assert not data["is_active"]

#Comprobar eliminación de un producto sin y con variantes
async def test_delete_product(
    admin_client,
    category_factory,
    product_factory,
    brand_factory
):

    brand = await brand_factory(name="asus", code="asu")
    cat = await category_factory(name="tarjeta de video", code="gpu")
    prod = await product_factory(
        name="Gaming GeForce RTX 4070 Twin Edge", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=cat, brand=brand
        )

    response = await admin_client.delete(
        f"/catalog/products/{prod.product_id}"
        )
    
    assert response.status_code == 204

    #TODO: Comprobar que no se puede eliminar un producto que tenga variantes
    
    # assert response.status_code == 409



async def test_deny_duplicated_product_creation(
    admin_client,
    brand_factory,
    category_factory,
    product_factory
):
    brand = await brand_factory(name="intel", code="int")
    cat = await category_factory(name="procesador", code="cpu")
    await product_factory(
        name="Core i9-14900K", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=cat, brand=brand
        )


    payload = {
        "name": "core i9-14900k", 
        "description": "lorem ipsum dolor sit amet consectetur adipiscing elit", 
        "category_id": str(cat.category_id), 
        "brand_id": str(brand.brand_id)
    }

    response = await admin_client.post("/catalog/products", json=payload)
    #Comprobar duplicados, en este caso ambos names son distintos(mayusculas y minusculas), pero el slug es el mismo
    assert response.status_code == 409

async def test_deny_duplicated_product_mofication(
    admin_client,
    brand_factory,
    category_factory,
    product_factory
):
    # Crea el producto que se va a editar
    brand = await brand_factory(name="intel", code="int")
    cat = await category_factory(name="procesador", code="cpu")
    prod = await product_factory(
        name="Core i9-14900K", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=cat, brand=brand
        )
    
    # Crea el producto "rival" (el que ya tiene el nombre ocupado)
    await product_factory(
        name="Core i5-14600K", 
        description="lorem ipsum dolor sit amet consectetur adipiscing elit", 
        category=cat, brand=brand
        )
    
    payload = {
        "name": "Core i5-14600K",
    }

    response = await admin_client.patch(
        f"/catalog/products/{prod.product_id}", 
        json=payload
    )
    
    #En este caso tanto el nombre como el slug se repiten
    assert response.status_code == 409


#Comprobar denegación inmediata a usuarios clientes
@pytest.mark.parametrize("endpoint, method", [
    ("/catalog/products", "post"),
    ("/catalog/products/999", "patch"),
    ("/catalog/products/999", "delete"),
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
