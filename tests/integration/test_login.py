import pytest

async def test_login_success(client, test_user):
    # 'test_user' ya viene con el usuario creado en la BD gracias al fixture
    
    user_data = test_user["user"]
    raw_password = test_user["password"]

    # 1. Armamos el payload con los datos del fixture
    payload = {
        "email": user_data.email, # Usamos el email que se creó en la BD
        "password": raw_password  # Usamos la contraseña plana
    }

    # 2. Hacemos la petición
    response = await client.post("/auth/login", json=payload)

    # 3. Validaciones
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"