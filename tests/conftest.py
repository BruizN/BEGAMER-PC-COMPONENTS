import os
from dotenv import load_dotenv
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from slugify import slugify



from app.main import app
from app.core.db import get_db 
from app.core.security import hash_password, create_access_token
from app.modules.auth.models import User
from app.modules.catalog.models import Category, Brand, Product

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise ValueError("❌ ERROR: No se encontró la variable TEST_DATABASE_URL. Revisa tu .env o tu CI.")


@pytest.fixture(scope="session")
def engine():
    return create_async_engine(TEST_DATABASE_URL, echo=False, future=True)

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
async def db_session(engine) -> AsyncGenerator[AsyncSession, None]:
    # Abrir una conexión a la BD
    async with engine.connect() as connection:
        
        # Inicia una Transacción
        transaction = await connection.begin()
        
        # Crea la sesión atada a esa conexión y transacción
        # NO cierra la transacción.
        session_factory = async_sessionmaker(
            bind=connection,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            join_transaction_mode="create_savepoint" # <--- crea un Savepoint
        )
        
        async with session_factory() as session:
            yield session # Aquí corren los tests

        # Al terminar el test, hacemos Rollback de la transacción Madre
        # Esto deshace TODO lo que pasó, incluidos los commits
        await transaction.rollback()

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
async def user_factory(db_session):
    async def _create_user(
        email: str = "default_user@test.com", 
        password: str = "password123", 
        role: str = "client",
        is_active: bool = True
    ) -> dict:
        
        hashed = hash_password(password)
        new_user = User(
            email=email,
            hashed_password=hashed,
            role=role,
            is_active=is_active
        )
        
        db_session.add(new_user)
        await db_session.commit()
        await db_session.refresh(new_user)
        
        return {"user": new_user, "password": password}

    return _create_user


@pytest.fixture
async def admin_user(user_factory):
    """
    Creamos un unico usuario con rol admin
    """
    data = await user_factory(
        email="admin_autenticado@test.com", 
        role="admin"
    )
    return data["user"]


@pytest.fixture
async def client_user(user_factory):
    """
    Creamos un unico usuario con rol cliente
    """
    data = await user_factory(
        email="soy_cliente_reutilizable@test.com", 
        role="client"
        )
    return data["user"]


@pytest.fixture
async def admin_client(client, admin_user):
    """
    1. Genera el token para el usuario admin.
    2. Lo inyecta en el cliente.
    3. Devuelve el cliente listo para usar.
    """
    access_token = create_access_token(
        data={"sub": str(admin_user.user_id), "role": admin_user.role} 
    )
    
    # Inyección
    client.headers.update({
        "Authorization": f"Bearer {access_token}"
    })
    
    return client

@pytest.fixture
async def user_client(client, client_user):
    """
    1. Genera el token para el usuario client.
    2. Lo inyecta en el cliente.
    3. Devuelve el cliente listo para usar.
    """
    access_token = create_access_token(
        data={"sub": str(client_user.user_id), "role": client_user.role}
        )
    # Inyección
    client.headers.update({
        "Authorization": f"Bearer {access_token}"
    })
    
    return client

@pytest.fixture
async def category_factory(db_session):
    async def _create_category(
        name: str, code: str, is_active: bool = True, 
        created_at: datetime | None = None, updated_at: datetime | None = None
        ):
        category = Category(
            name=name, code=code.upper(), is_active=is_active, 
            created_at=created_at, updated_at=updated_at
            ) #Reglas de negocio
        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)
        return category
    return _create_category

@pytest.fixture
async def brand_factory(db_session):
    async def _create_brand(
        name: str, code: str, is_active: bool = True, 
        created_at: datetime | None = None, updated_at: datetime | None = None
        ):

        brand = Brand(
            name=name, code=code.upper(), is_active=is_active, 
            created_at=created_at, updated_at=updated_at
            ) 
        db_session.add(brand)
        await db_session.commit()
        await db_session.refresh(brand)
        return brand
    return _create_brand

@pytest.fixture
async def product_factory(db_session):
    async def _create_product(
        name: str, 
        description: str, 
        category: Category, 
        brand: Brand, 
        is_active: bool = True, 
        created_at: datetime | None = None, 
        updated_at: datetime | None = None
        ):

        nombre_producto = name
        nombre_marca = brand.name

        if nombre_producto.lower().startswith(nombre_marca.lower()):
            slug_text = f"{category.code} {nombre_producto}" 
        else:
            slug_text = f"{category.code} {nombre_marca} {nombre_producto}"

        generated_slug = slugify(slug_text)
        product = Product(
            name=name, 
            description=description, 
            slug=generated_slug, 
            category_id=category.category_id, 
            brand_id=brand.brand_id, 
            is_active=is_active, 
            created_at=created_at, 
            updated_at=updated_at
            )
        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product)
        return product
    return _create_product