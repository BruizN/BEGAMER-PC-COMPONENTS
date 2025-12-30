import os
from dotenv import load_dotenv
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession


from app.main import app
from app.core.db import get_db 
from app.core.security import hash_password
from app.modules.auth.models import User

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise ValueError("❌ ERROR: No se encontró la variable TEST_DATABASE_URL. Revisa tu .env o tu CI.")


test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)


TestAsyncSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)



# Setup de la Base de Datos 
@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    async with test_engine.begin() as conn:
        # Limpia por si acaso quedó basura de antes
        await conn.run_sync(SQLModel.metadata.drop_all)
        # Crea todas las tablas
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # Al terminar todos los tests, borra todo
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await test_engine.dispose()

# Fixture de Sesión 
@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionLocal() as session:
        yield session

# Fixture del Cliente
@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    # Función  que reemplaza a get_db
    async def override_get_db():
        yield db_session

    # Intercepta la dependencia
    app.dependency_overrides[get_db] = override_get_db

    # Crea el cliente HTTP asíncrono
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()

@pytest.fixture
async def test_user(db_session):
    password_raw = "password_segura_123"
    hashed = hash_password(password_raw)

    new_user = User(
        email="usuario_test@ejemplo.com",
        hashed_password=hashed,
        role="client",
        is_active=True
    )

    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)

    return {"user": new_user, "password": password_raw}