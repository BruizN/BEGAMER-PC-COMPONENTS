from fastapi import APIRouter
from app.modules.catalog import service as serv
from app.core.dependencies import SessionDep, CurrentAdmin, CurrentUserOptional
import uuid
from fastapi import status, Query
from app.modules.catalog.schemas import (
    ProductVariantCreate, 
    ProductVariantRead, 
    ProductVariantUpdate
)

router = APIRouter(tags=["Variants"])

@router.post(
    "/products/{product_id}/variants",
    response_model=ProductVariantRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new variant for your products"
)
async def create_variant(
    session: SessionDep,
    admin: CurrentAdmin,
    product_id: uuid.UUID,
    body: ProductVariantCreate
):
    return await serv.create_variant(session, product_id, body)

@router.get(
    "/products/{product_id}/variants",
    response_model=list[ProductVariantRead],
    status_code=status.HTTP_200_OK,
    summary="Get all variants for a product"
)
async def list_variants(
    session: SessionDep,
    user: CurrentUserOptional,
    product_id: uuid.UUID,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=0, le=100),
    is_active: bool | None = None
):
    # Determinar si es admin
    is_admin_user = user is not None and user.role == "admin"
    
    # Lógica de filtrado de seguridad
    filter_active_state = True 

    if is_admin_user:
        filter_active_state = is_active

    return await serv.list_variants(
        session, 
        offset=offset, 
        limit=limit, 
        is_active=filter_active_state,
        product_id=product_id
    )

@router.get(
    "/variants/{variant_id}",
    response_model=ProductVariantRead,
    status_code=status.HTTP_200_OK,
    summary="Get a variant by ID"
)
async def get_variant(
    session: SessionDep,
    user: CurrentUserOptional,
    variant_id: uuid.UUID,
):
    is_admin = False
    
    if user is not None and user.role == "admin":
        is_admin = True
    
    should_filter_active = not is_admin 
    return await serv.get_variant(
        session, 
        variant_id, 
        only_active=should_filter_active
    )

@router.patch(
    "/variants/{variant_id}",
    response_model=ProductVariantRead,
    status_code=status.HTTP_200_OK,
    summary="Update a variant"
)
async def update_variant(
    session: SessionDep,
    admin: CurrentAdmin,
    variant_id: uuid.UUID,
    body: ProductVariantUpdate
):
    return await serv.update_variant(session, variant_id, body)

@router.delete(
    "/variants/{variant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an existing variant by ID, if the variant is associated with orders, it will not be deleted"
)
async def delete_variant(
    session: SessionDep,
    admin: CurrentAdmin,
    variant_id: uuid.UUID
):
    return await serv.delete_variant(session, variant_id)
