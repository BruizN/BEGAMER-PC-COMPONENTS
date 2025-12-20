from app.core.security import hash_password, verify_password, create_access_token
import jwt
from app.core.config import settings


def test_correct_hash():
    hashed_password = hash_password("HOLAmundo123")
    verify = verify_password("HOLAmundo123", hashed_password)
    assert verify

def test_wrong_hash():
    hashed_password = hash_password("CHAOmundo123")
    verify = verify_password("HOLAmundo123", hashed_password)
    assert not verify

def test_create_access_token():
    data = {"sub": "usuario@test.com"}
    token = create_access_token(data)

    payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
    assert payload["sub"] == "usuario@test.com"
    assert "exp" in payload