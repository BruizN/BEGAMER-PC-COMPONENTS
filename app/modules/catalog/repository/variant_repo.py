from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
import uuid
from app.modules.catalog.models import ProductVariant
from app.modules.catalog.schemas import ProductVariantCreate
from app.modules.catalog.exceptions import (
    SkuAlreadyExistsError,
    )


async def add_variant(
    session: AsyncSession,
    new_variant: ProductVariantCreate
) -> ProductVariant:
    session.add(new_variant)
    try:
        await session.flush()
    except IntegrityError as e:
        error_msg = str(e.orig) 

        if "sku" in error_msg: 
             raise SkuAlreadyExistsError(
                f"The variant with SKU '{new_variant.sku}' already exists."
             )     
             
        raise e 

    await session.refresh(new_variant, ["product"])
    return new_variant