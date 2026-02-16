from app.modules.catalog import service as serv
from app.core.dependencies import SessionDep, CurrentAdmin, CurrentUserOptional
import uuid
from fastapi import APIRouter, status, Query
from app.modules.catalog.schemas import (
    CategoryCreate, 
    CategoryRead, 
    CategoryUpdate
)

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post(
    "/",
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
    "/{category_id}",
    response_model=CategoryRead,
    summary="Get a category by its id (Admins see all, Guests see active only)"
)
async def get_category(
    session: SessionDep,
    category_id: uuid.UUID,
    user: CurrentUserOptional
):
    is_admin = False
    
    if user is not None and user.role == "admin":
        is_admin = True
    
    should_filter_active = not is_admin 
    return await serv.get_category(
        session, 
        category_id, 
        only_active=should_filter_active
    )

@router.get(
    "/",
    response_model=list[CategoryRead],
    summary="List categories (Admins see all, Guests see active only)"
)
async def list_categories(
    session: SessionDep,
    user: CurrentUserOptional,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=0, le=100),
    is_active: bool | None = None
):
    is_admin = False
    
    if user is not None and user.role == "admin":
        is_admin = True
    
    filter_active_state = True 
    if is_admin:
        filter_active_state = is_active

    return await serv.list_categories(
        session, 
        offset=offset, 
        limit=limit, 
        is_active=filter_active_state
    )

@router.patch(
    "/{category_id}",
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
    "/{category_id}",
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