import os
import asyncio
import logging
from sqlmodel import select
from dotenv import load_dotenv

from app.core.db import AsyncSessionLocal
from app.modules.auth.models import User
from app.core.security import hash_password
from fastapi.concurrency import run_in_threadpool

load_dotenv()
admin_email = os.getenv("FIRST_SUPERUSER_EMAIL")
admin_pass = os.getenv("FIRST_SUPERUSER_PASSWORD")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_superuser():
    """
    Crea un superusuario inicial si no existe
    """
    async with AsyncSessionLocal() as session:
        try:
            logger.info("Verificando existencia de Admin...")

            query = select(User).where(User.email == admin_email)
            result = await session.execute(query)
            user = result.first()

            if user:
                logger.info(f"El usuario admin {admin_email} ya existe")
                return

            logger.info("Creando usuario Admin...")

            new_admin = User(
                email=admin_email,
                role="admin",
                hashed_password= await run_in_threadpool(hash_password, admin_pass),
                is_active=True
            )

            session.add(new_admin)
            await session.commit()

            logger.info(f"Admin creado exitosamente! Email: {admin_email}")

        except Exception as e:
            logger.error(f"Error creando el admin : {e}")
            await session.rollback()
            raise

async def main():
    logger.info("Iniciando script de semilla...")
    await create_superuser()
    logger.info("Script finalizado.")

if __name__ == "__main__":
    asyncio.run(main())