from datetime import datetime, timedelta, timezone
import uuid6
import jwt
from app.core.config import settings

async def test_protected_route_rejects_expired_token(client):
    """
    Simulamos un token que expiró hace 5 minutos y tratamos de usarlo
    """
    expired_payload = {
        "sub": str(uuid6.uuid7()),
        "role": "admin",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=5)
    }

    expired_token = jwt.encode(
        expired_payload,
        settings.jwt_secret,
        algorithm=settings.jwt_alg
    )

    response = await client.post(
        "/catalog/categories/",
        headers={"Authorization": f"bearer {expired_token}"}
    )
#   Validar que la API lo rechace
    assert response.status_code == 401
    assert "Expired token" in response.text

async def test_protected_route_rejects_tampered_token(client):
    """
    Simulamos un token con datos válidos, pero firmado con una 
    SECRET_KEY diferente a la del servidor. Esto simula un ataque
    donde alguien intenta falsificar credenciales.
    """
    payload = {
        "sub": str(uuid6.uuid7()),
        "role": "admin",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    fake_secret_key = "MyOWNpassword"

    tampered_token = jwt.encode(
        payload,
        fake_secret_key,
        algorithm=settings.jwt_alg
    )

    response = await client.post(
        "/catalog/categories/",
        headers={"Authorization": f"bearer {tampered_token}"}
    )

    assert response.status_code == 401
    assert "Invalid token" in response.text