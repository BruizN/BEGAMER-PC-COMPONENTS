from app.modules.catalog import repository as repo
from app.modules.catalog.models import Category
from app.modules.catalog.schemas import CategoryCreate, CategoryUpdate
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