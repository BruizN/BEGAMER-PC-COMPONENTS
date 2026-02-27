from app.modules.catalog.models import ProductImage
from sqlmodel.ext.asyncio.session import AsyncSession
from app.modules.catalog.exceptions import ImageNotFoundError
from sqlalchemy import update
from sqlmodel import select
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
    variant_id: uuid.UUID | None = None
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

async def get_image_by_id(
    session: AsyncSession,
    image_id: uuid.UUID
) -> ProductImage:
    query = select(ProductImage).where(ProductImage.image_id == image_id)
    
    result = await session.exec(query)
    image = result.first()
    if not image:
        raise ImageNotFoundError("Image not found")
    return image


async def remove_image(
    session: AsyncSession,
    image_id: uuid.UUID
) -> None:
    image = await session.get(ProductImage, image_id)
    
    await session.delete(image)

    return  