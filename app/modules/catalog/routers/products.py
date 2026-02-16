from app.modules.catalog import service as serv
from app.core.dependencies import SessionDep, CurrentAdmin, CurrentUserOptional
import uuid
from fastapi import APIRouter, status, Query
from app.modules.catalog.schemas import (
    ProductCreate, 
    ProductRead, 
    ProductUpdate
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product for your catalog"
)
async def create_product(
    session: SessionDep,
    admin: CurrentAdmin,
    body: ProductCreate
):
    return await serv.create_product(session, body)

@router.get(
    "/{product_id}",
    response_model=ProductRead,
    summary="Get a product by its id (Admins see all, Guests see active only)"
)
async def get_product(
    session: SessionDep,
    product_id: uuid.UUID,
    user: CurrentUserOptional
):
    is_admin = False
    
    if user is not None and user.role == "admin":
        is_admin = True
    
    should_filter_active = not is_admin 
    return await serv.get_product(
        session, 
        product_id, 
        only_active=should_filter_active
    )

@router.get(
    "/",
    response_model=list[ProductRead],
    summary="List products (Admins see all, Guests see active only)"
)
async def list_products(
    session: SessionDep,
    user: CurrentUserOptional,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=0, le=100),
    category_id: uuid.UUID | None = None,
    brand_id: uuid.UUID | None = None,
    search: str | None = None,
    is_active: bool | None = None
):
    # Determinar si es admin
    is_admin_user = user is not None and user.role == "admin"
    
    # Lógica de filtrado de seguridad
    filter_active_state = True 

    if is_admin_user:
        filter_active_state = is_active

    return await serv.list_products(
        session, 
        offset=offset, 
        limit=limit, 
        is_active=filter_active_state,
        category_id=category_id,
        brand_id=brand_id,
        search=search
    )

@router.patch(
    "/{product_id}",
    response_model=ProductRead,
    summary="Update an existing product by its id"
)
async def edit_product(
    session: SessionDep,
    admin: CurrentAdmin,
    product_id: uuid.UUID,
    body: ProductUpdate
):
    return await serv.edit_product(session, product_id, body)

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an existing product by its id, if the product has variants, it will not be deleted"
)
async def delete_product(
    session: SessionDep,
    admin: CurrentAdmin,
    product_id: uuid.UUID
):
    await serv.delete_product(session, product_id)
    return
