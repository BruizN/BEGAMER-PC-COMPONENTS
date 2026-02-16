from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
import uuid
from app.modules.catalog.models import Brand
from app.modules.catalog.exceptions import (
    BrandAlreadyExistsError,
    BrandNotFoundError,
    BrandNotEmptyError,
    )


async def add_brand(
    session: AsyncSession,
    new_brand: Brand
) -> Brand:
    session.add(new_brand)
    try:
        await session.flush()
    except IntegrityError as e:
        error_msg = str(e.orig) 

        if "code" in error_msg: 
             raise BrandAlreadyExistsError(
                f"The brand with the code '{new_brand.code}' already exists."
             )

        elif "name" in error_msg:
             raise BrandAlreadyExistsError(
                f"The brand with the name '{new_brand.name}' already exists."
             )           
             
        raise e 
    return new_brand

async def get_brand(
    session: AsyncSession,
    brand_id: uuid.UUID,
    only_active: bool
) -> Brand:
    query = select(Brand).where(Brand.brand_id == brand_id)
    if only_active:
        query = query.where(Brand.is_active)
    
    result = await session.exec(query)
    brand = result.first()
    if not brand:
        raise BrandNotFoundError("Brand not found")
    return brand

async def get_all_brands(
    session: AsyncSession,
    offset: int,
    limit: int,
    is_active: bool | None = True
) -> list[Brand]:
    query = select(Brand)
    
    if is_active is not None:
        query = query.where(Brand.is_active == is_active)
        
    query = query.order_by(Brand.created_at.desc())
    query = query.offset(offset).limit(limit)
    result = await session.exec(query)
    return list(result.all())

async def update_brand(
    session: AsyncSession,
    brand_id: uuid.UUID,
    update_data: dict
) -> Brand:
    brand = await session.get(Brand, brand_id)

    if not brand:
        raise BrandNotFoundError("Brand not found")

    brand.sqlmodel_update(update_data)

    session.add(brand)
    try:
        await session.flush()
    except IntegrityError as e:
        error_msg = str(e.orig) 

        if "code" in error_msg: 
             raise BrandAlreadyExistsError(
                f"The brand with the code '{update_data["code"]}' already exists."
             )

        elif "name" in error_msg:
             raise BrandAlreadyExistsError(
                f"The brand with the name '{update_data["name"]}' already exists."
             )           
        raise e 
        
    await session.refresh(brand)
    return brand

async def remove_brand(
    session: AsyncSession,
    brand_id: uuid.UUID
) -> None:
    brand = await session.get(Brand, brand_id)

    if not brand:
        raise BrandNotFoundError("Brand not found")
    
    await session.delete(brand)

    try:
        await session.flush()

    except IntegrityError as e:
        if "foreign key constraint" in str(e.orig):
            raise BrandNotEmptyError(
                "Cannot delete brand: The brand contains products. Please archive the brand instead."
                )
        raise e

    return  