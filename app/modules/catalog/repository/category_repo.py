from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
import uuid
from app.modules.catalog.models import Category
from app.modules.catalog.exceptions import (
    CategoryAlreadyExistsError, 
    CategoryNotFoundError, 
    CategoryNotEmptyError,
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
    is_active: bool | None = True
) -> list[Category]:
    query = select(Category)
    
    if is_active is not None:
        query = query.where(Category.is_active == is_active)
    
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
            raise CategoryNotEmptyError("Cannot delete category: The category contains products. Please archive the category instead.")
        raise e

    return