from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
import uuid
from app.modules.catalog.models import Category
from app.modules.catalog.exceptions import CategoryAlreadyExistsError, CategoryNotFoundError, CategoryNotEmptyError

async def add_category(
    session: AsyncSession,
    new_category: Category
) -> Category:
    session.add(new_category)
    try:
        await session.flush()
    except IntegrityError as e:
        if "unique constraint" in str(e.orig): 
             raise CategoryAlreadyExistsError("Category already exists")
        raise e 
    return new_category

async def get_all_categories(
    session: AsyncSession,
) -> list[Category]:
    result = await session.exec(select(Category))
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
        if "unique constraint" in str(e.orig): 
             raise CategoryAlreadyExistsError("Category already exists")
        raise e 
        
    return category

async def remove_category(
    session: AsyncSession,
    category_id: uuid.UUID
) -> None:
    category = await session.get(Category, category_id)

    if not category:
        raise CategoryNotFoundError("Category not found")

    session.delete(category)
    
    try:
        await session.flush()
    except IntegrityError as e:
        if "foreign key constraint" in str(e.orig):
            raise CategoryNotEmptyError("Cannot be deleted: The category contains products.")
        raise e 
        
    return