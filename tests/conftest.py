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


@pytest.fixture(scope="session")
def engine():
    return create_async_engine(TEST_DATABASE_URL, echo=False, future=True)

@pytest.fixture(scope="session")
def async_session_factory(engine):
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )

@pytest.fixture(scope="session", autouse=True)
async def setup_test_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()

@pytest.fixture(scope="function")
async def db_session(async_session_factory) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
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