from fastapi import APIRouter
from app.modules.catalog import service as serv
from app.core.dependencies import SessionDep, CurrentAdmin, CurrentUserOptional
import uuid
from fastapi import APIRouter, status, Query
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