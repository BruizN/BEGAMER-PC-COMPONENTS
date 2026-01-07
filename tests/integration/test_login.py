import pytest
import jwt
from app.core.config import settings



"""
Happy path. Verificamos construcción correcta del token tras un login con 
credenciales validas.
"""
#Permite correr el mismo test varias veces con diferentes datos.
@pytest.mark.parametrize("email, password, role_expected", [
    ("client_login@begamer.com", "pass_cliente_123", "client"),
    ("admin_login@begamer.com", "pass_admin_123", "admin"),
])
async def test_login_ok(
    client, 
    user_factory, 
    email, 
    password, 
    role_expected
):
    await user_factory(
        email=email, 
        password=password,
        role=role_expected
    )

    payload = {
        "email": email,  
        "password": password     
    }
    response = await client.post("/auth/login", json=payload)
    
    assert response.status_code == 200
    token_data = response.json()
    decoded = jwt.decode(
        token_data["access_token"], 
        settings.jwt_secret, 
        algorithms=[settings.jwt_alg]
    )
    assert token_data["token_type"] == "bearer"
    assert decoded["role"] == role_expected
    assert "exp" in decoded



"""
Edge case. Verificamos que la API deniegue credenciales invalidas
(Contraseña incorrecta y Usuario no existente)
"""
@pytest.mark.parametrize("email, password", [
    # Caso 1: Usuario existe, contraseña mala
    ("client_login@begamer.com", "CLAVE_MALA"), 
    # Caso 2: Usuario NO existe (email random), contraseña da igual
    ("no_existo@begamer.com", "pass123"), 
])
async def test_login_failures(
    client, 
    user_factory, 
    email, 
    password,
):
    # Creamos un usuario "base" correcto en la BD para probar el conflicto
    await user_factory(email="client_login@begamer.com", password="password_real")

    payload = {"email": email, "password": password}
    
    response = await client.post("/auth/login", json=payload)
    
    assert response.status_code == 401


