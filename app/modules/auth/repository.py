from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.modules.auth.models import User


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    query = select(User).where(User.email == email)
    result = await session.exec(query)

    return result.first()