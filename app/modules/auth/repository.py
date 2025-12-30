from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.modules.auth.models import User
import uuid


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    query = select(User).where(User.email == email)
    result = await session.exec(query)

    return result.first()

async def get_user_by_id(
    session: AsyncSession, 
    user_id: uuid.UUID
    ) -> User | None:
    query = select(User).where(User.user_id == user_id)
    result = await session.exec(query)

    return result.first()