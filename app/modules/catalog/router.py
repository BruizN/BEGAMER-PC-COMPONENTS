from fastapi import APIRouter, status
from app.modules.catalog.schemas import (
    CategoryCreate, 
    CategoryRead, 
    CategoryUpdate
)
from app.core.dependencies import SessionDep
from app.modules.catalog import service as serv
from app.core.dependencies import CurrentAdmin
import uuid

router = APIRouter()

@router.post(
    "/categories",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category for your products"
)
async def create_category(
    session: SessionDep,
    admin: CurrentAdmin,
    body: CategoryCreate
):
    return await serv.create_category(session, body)

@router.get(
    "/categories",
    response_model=list[CategoryRead],
    summary="List all registered categories"
)
async def list_categories(
    session: SessionDep,
    admin: CurrentAdmin
):
    return await serv.list_categories(session)

@router.put(
    "/categories/{category_id}",
    response_model=CategoryRead,
    summary="Update an existing category by its id"
)
async def edit_category(
    session: SessionDep,
    admin: CurrentAdmin,
    category_id: uuid.UUID,
    body: CategoryUpdate
):
    return await serv.edit_category(session, category_id, body)

@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an existing category by its id"
)
async def delete_category(
    session: SessionDep,
    admin: CurrentAdmin,
    category_id: uuid.UUID
) -> None:
    await serv.delete_category(session, category_id)
    return