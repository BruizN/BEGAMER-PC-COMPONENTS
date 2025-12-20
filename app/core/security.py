from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from app.core.config import settings
from fastapi.security import HTTPBearer

http_bearer = HTTPBearer(auto_error=True)


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__type="ID",
    argon2__memory_cost=65536,
    argon2__time_cost=3,
    argon2__parallelism=2,
)

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_min)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_alg)