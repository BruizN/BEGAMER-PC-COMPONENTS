from app.modules.catalog.models import ProductImage
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import update
import uuid

async def add_image(
    session: AsyncSession,
    new_image: ProductImage
) -> ProductImage:
    session.add(new_image)
    await session.flush()
    return new_image

async def unset_main_image(
    session: AsyncSession,
    product_id: uuid.UUID,
    variant_id: uuid.UUID
) -> None:
    """
    Unset the flag 'is_main' for all images of a product or variant.
    """
    query = update(ProductImage).where(ProductImage.product_id == product_id)

    if variant_id:
        query = query.where(ProductImage.variant_id == variant_id)
    else:
        query = query.where(ProductImage.variant_id.is_(None))

    query = query.values(is_main=False)
    await session.execute(query)