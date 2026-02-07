from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
import uuid
from app.modules.catalog.models import Category, Brand
from app.modules.catalog.exceptions import (
    CategoryAlreadyExistsError, 
    CategoryNotFoundError, 
    CategoryNotEmptyError,
    BrandAlreadyExistsError,
    BrandNotFoundError,
    BrandNotEmptyError
    )

async def add_category(
    session: AsyncSession,
    new_category: Category
) -> Category:
    session.add(new_category)
    try:
        await session.flush()
    except IntegrityError as e:
        error_msg = str(e.orig) 
        # Duplicado por CODIGO
        if "code" in error_msg: 
             raise CategoryAlreadyExistsError(
                f"The category with the code '{new_category.code}' already exists."
             )
        # Duplicado por NOMBRE
        elif "name" in error_msg:
             raise CategoryAlreadyExistsError(
                f"The category with the name '{new_category.name}' already exists."
             )           
             
        raise e 
        
    return new_category

async def get_category(
    session: AsyncSession,
    category_id: uuid.UUID,
    only_active: bool
) -> Category:
    query = select(Category).where(Category.category_id == category_id)
    if only_active:
        query = query.where(Category.is_active)
    
    result = await session.exec(query)
    category = result.first()
    if not category:
        raise CategoryNotFoundError("Category not found")
    return category

async def get_all_categories(
    session: AsyncSession,
    offset: int,
    limit: int,
    only_active: bool = True
) -> list[Category]:
    query = select(Category)
    if only_active:
        query = query.where(Category.is_active)
    
    query = query.order_by(Category.created_at.desc())
    query = query.offset(offset).limit(limit)
    result = await session.exec(query)
    return list(result.all())

async def update_category(
    session: AsyncSession,
    category_id: uuid.UUID,
    update_data: dict
) -> Category:
    category = await session.get(Category, category_id)

    if not category:
        raise CategoryNotFoundError("Category not found")
        
    category.sqlmodel_update(update_data)
    
    session.add(category)
    try:
        await session.flush()
    except IntegrityError as e:
        error_msg = str(e.orig) 

        if "code" in error_msg: 
             raise CategoryAlreadyExistsError(
                f"The category with the code '{update_data["code"]}' already exists."
             )

        elif "name" in error_msg:
             raise CategoryAlreadyExistsError(
                f"The category with the name '{update_data["name"]}' already exists."
             )           
        raise e 
        
    await session.refresh(category)
    return category

async def remove_category(

    session: AsyncSession,

    category_id: uuid.UUID

) -> None:

    category = await session.get(Category, category_id)

    if not category:
        raise CategoryNotFoundError("Category not found")

    await session.delete(category)

    try:
        await session.flush()

    except IntegrityError as e:
        if "foreign key constraint" in str(e.orig):
            raise CategoryNotEmptyError("Cannot be deleted: The category contains products.")
        raise e

    return

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
    only_active: bool = True
) -> list[Brand]:
    query = select(Brand)
    if only_active:
        query = query.where(Brand.is_active)
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
                "Cannot be deleted: The brand contains products."
                )
        raise e

    return  
