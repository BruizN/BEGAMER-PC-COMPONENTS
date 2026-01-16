from fastapi import APIRouter, status
from app.modules.catalog.schemas import (
    CategoryCreate, 
    CategoryRead, 
    CategoryUpdate,
    BrandCreate,
    BrandRead,
    BrandUpdate
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
):
    return await serv.list_categories(session)

@router.patch(
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

@router.post(
    "/brands",
    response_model=BrandRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new brand for your products"
)
async def create_brand(
    session: SessionDep,
    admin: CurrentAdmin,
    body: BrandCreate
):
    return await serv.create_brand(session, body)

@router.get(
    "/brands",
    response_model=list[BrandRead],
    summary="List all registered brands"
)
async def list_brands(
    session: SessionDep
):
    return await serv.list_brands(session)

@router.patch(
    "/brands/{brand_id}",
    response_model=BrandRead,
    summary="Update an existing brand by its id"
)
async def edit_brand(
    session: SessionDep,
    admin: CurrentAdmin,
    brand_id: uuid.UUID,
    body: BrandUpdate
):
    return await serv.edit_brand(session, brand_id, body)

@router.delete(
    "/brands/{brand_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an existing brand by its id"
)
async def delete_brand(
    session: SessionDep,
    admin: CurrentAdmin,
    brand_id: uuid.UUID
):
    await serv.delete_brand(session, brand_id)
    return