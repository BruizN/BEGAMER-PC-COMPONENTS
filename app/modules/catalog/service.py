from app.modules.catalog import repository as repo
from app.modules.catalog.models import Category, Brand
from app.modules.catalog.schemas import (
    CategoryCreate, 
    CategoryUpdate,
    BrandCreate,
    BrandUpdate
)
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid

async def create_category(
    session: AsyncSession,
    category_data: CategoryCreate
) -> Category:
    new_category = Category.model_validate(category_data)
    
    return await repo.add_category(session, new_category)
    
async def list_categories(
    session: AsyncSession,
) -> list[Category]:
    return await repo.get_all_categories(session)

async def edit_category(
    session: AsyncSession,
    category_id: uuid.UUID,
    edit_category_data: CategoryUpdate 
) -> Category:
    update_data = edit_category_data.model_dump()
    return await repo.update_category(session, category_id, update_data)

async def delete_category(
    session: AsyncSession, 
    category_id: uuid.UUID
) -> None:
    await repo.remove_category(session, category_id)
    return

async def create_brand(
    session: AsyncSession,
    brand_data: BrandCreate
) -> Brand:
    new_brand = Brand.model_validate(brand_data)

    return await repo.add_brand(session, new_brand)

async def list_brands(
    session: AsyncSession,
) -> list[Brand]:
    return await repo.get_all_brands(session)

async def edit_brand(
    session: AsyncSession,
    brand_id: uuid.UUID,
    edit_brand_data: BrandUpdate
) -> Brand:
    update_data = edit_brand_data.model_dump()
    return await repo.update_brand(session, brand_id, update_data)

async def delete_brand(
    session: AsyncSession,
    brand_id: uuid.UUID
) -> None:
    await repo.remove_brand(session, brand_id)
    return 