


async def test_guest_add_item_to_cart(client, override_redis, variant_factory):
    variant = await variant_factory()
    
    headers = {"X-Guest-Session-ID": "test-guest-123"}
    payload = {
        "variant_id": str(variant.variant_id),
        "quantity": 2
    }
    
    response = await client.post(
        "/cart/items",
        json=payload,
        headers=headers
    )
    
    assert response.status_code == 201
    assert response.json()["current_quantity"] == 2


async def test_cart_business_rule_max_10_items(client, override_redis, variant_factory):
    variant = await variant_factory()
    headers = {"X-Guest-Session-ID": "test-guest-123"}
    
    # Intentar agregar 11 unidades (El límite es 10)
    payload = {
        "variant_id": str(variant.variant_id),
        "quantity": 11 
    }
    
    response = await client.post(
        "/cart/items",
        json=payload,
        headers=headers
    )
    
    assert response.status_code == 422 


async def test_merge_cart_on_login(client, override_redis, user_factory, variant_factory, redis_mock):
    user_data = await user_factory(email="mergetest@begamer.cl", password="password123")
    user = user_data["user"]
    variant = await variant_factory()
    variant_id_str = str(variant.variant_id)

    guest_session = "guest-merge-99"

    await redis_mock.hset(f"cart:guest:{guest_session}", variant_id_str, 2)
    
    await redis_mock.hset(f"cart:user:{user.user_id}", variant_id_str, 3)

    login_payload = {
        "email": "mergetest@begamer.cl", 
        "password": "password123"
    }
    headers = {
        "X-Guest-Session-ID": guest_session
    }
    
    response = await client.post(
        "/auth/login",
        json=login_payload, 
        headers=headers
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

    
    user_cart = await redis_mock.hgetall(f"cart:user:{user.user_id}")
    guest_cart_exists = await redis_mock.exists(f"cart:guest:{guest_session}")

    assert user_cart[variant_id_str] == "5"
    
    # El carrito del visitante debe haber sido destruido
    assert guest_cart_exists == 0