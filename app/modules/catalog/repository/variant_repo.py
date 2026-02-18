from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
import uuid
from app.modules.catalog.models import ProductVariant, Product
from app.modules.catalog.schemas import ProductVariantCreate
from app.modules.catalog.exceptions import (
    SkuAlreadyExistsError,
    VariantNotFoundError,
    VariantNotEmptyError
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
    
async def get_all_product_variants(
    session: AsyncSession,
    offset: int,
    limit: int,
    product_id: uuid.UUID,
    is_active: bool | None = None
) -> list[ProductVariant]:
    
    query = (
        select(ProductVariant)
        .options(
            joinedload(ProductVariant.product).joinedload(Product.category),
            joinedload(ProductVariant.product).joinedload(Product.brand)
        )
    )

    if is_active is not None:
        query = query.where(ProductVariant.is_active == is_active)

    if product_id:
        query = query.where(ProductVariant.product_id == product_id)

    query = query.order_by(ProductVariant.created_at.desc())
    query = query.offset(offset).limit(limit)
    
    result = await session.exec(query)
    return list(result.unique().all())

async def get_variant_by_id(
    session: AsyncSession,
    variant_id: uuid.UUID,
    only_active: bool
) -> ProductVariant:
    query = (
        select(ProductVariant)
        .where(ProductVariant.variant_id == variant_id)
        .options(
            joinedload(ProductVariant.product).joinedload(Product.category),
            joinedload(ProductVariant.product).joinedload(Product.brand)
        )
    )

    if only_active:
        query = query.where(ProductVariant.is_active)

    result = await session.exec(query)
    variant = result.first()

    if not variant:
        raise VariantNotFoundError(f"Variant with ID '{variant_id}' not found.")

    return variant

async def update_variant(
    session: AsyncSession,
    variant_id: uuid.UUID,
    update_data: dict
) -> ProductVariant:
    variant = await session.get(ProductVariant, variant_id)

    if not variant:
        raise VariantNotFoundError("Variant not found")

    variant.sqlmodel_update(update_data)

    session.add(variant)
    try:
        await session.flush()
    except IntegrityError as e:
        error_msg = str(e.orig) 

        if "sku" in error_msg: 
             raise SkuAlreadyExistsError(
                f"The variant with SKU '{update_data["sku"]}' already exists."
             )           
             
        raise e 

    await session.refresh(variant, ["product", "updated_at"])
    return variant

async def remove_variant(
    session: AsyncSession,
    variant_id: uuid.UUID
) -> None:
    variant = await session.get(ProductVariant, variant_id)

    if not variant:
        raise VariantNotFoundError("Variant not found")
    
    await session.delete(variant)

    try:
        await session.flush()

    except IntegrityError as e:
        if "foreign key constraint" in str(e.orig):
            raise VariantNotEmptyError(
                "Cannot delete variant: It is associated with existing orders. Please archive it instead."
                )
        raise e

    return  
