from app.modules.catalog import service as serv
from app.core.dependencies import SessionDep, CurrentAdmin, CurrentUserOptional
import uuid
from fastapi import APIRouter, status, Query
from app.modules.catalog.schemas import (
    BrandCreate, 
    BrandRead, 
    BrandUpdate
)

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.post(
    "/",
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
    "/{brand_id}",
    response_model=BrandRead,
    summary="Get a brand by its id (Admins see all, Guests see active only)"
)
async def get_brand(
    session: SessionDep,
    brand_id: uuid.UUID,
    user: CurrentUserOptional
):
    is_admin = False
    
    if user is not None and user.role == "admin":
        is_admin = True
    
    should_filter_active = not is_admin 
    return await serv.get_brand(
        session, 
        brand_id, 
        only_active=should_filter_active
    )

@router.get(
    "/",
    response_model=list[BrandRead],
    summary="List brands (Admins see all, Guests see active only)"
)
async def list_brands(
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
        
    return await serv.list_brands(
        session, 
        offset=offset, 
        limit=limit, 
        is_active=filter_active_state
    )
@router.patch(
    "/{brand_id}",
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
    "/{brand_id}",
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