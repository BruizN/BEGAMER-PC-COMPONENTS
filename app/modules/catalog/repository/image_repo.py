from app.modules.catalog.models import ProductImage
from sqlmodel.ext.asyncio.session import AsyncSession

async def add_image(
    session: AsyncSession,
    new_image: ProductImage
) -> ProductImage:
    session.add(new_image)
    await session.flush()
    return new_image