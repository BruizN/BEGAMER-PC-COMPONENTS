import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.core.db import get_db 
from app.core.config import settings


TEST_DATABASE_URL = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@localhost:5433/begamer_test"


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