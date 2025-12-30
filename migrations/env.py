import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Importaciones Propias
from app.core.config import settings
from sqlmodel import SQLModel

# Modelos 
from app.modules.auth.models import User # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

SQLModel.metadata.naming_convention = naming_convention
# Metadata de SQLModel
target_metadata = SQLModel.metadata

# INYECCIÓN DE LA URL
config.set_main_option("sqlalchemy.url", str(settings.postgres_url))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        # Habilitar detección de cambios de tipo (VARCHAR, INT, ENUM, etc.)
        compare_type=True,
        # Habilitar detección de cambios en defaults (server_default)
        compare_server_default=True,)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    
    # Configurar el motor Async con la URL inyectada
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Alembic es síncrono por dentro, así que se usa run_sync
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()



if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())