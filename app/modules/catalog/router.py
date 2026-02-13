from fastapi import APIRouter, status, Query
from app.modules.catalog.schemas import (
    CategoryCreate, 
    CategoryRead, 
    CategoryUpdate,
    BrandCreate,
    BrandRead,
    BrandUpdate,
    ProductCreate,
    ProductRead,
    ProductUpdate
)
from app.core.dependencies import SessionDep
from app.modules.catalog import service as serv
from app.core.dependencies import CurrentAdmin, CurrentUserOptional
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
    "/categories/{category_id}",
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
    "/categories",
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
    "/brands/{brand_id}",
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
    "/brands",
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

@router.post(
    "/products",
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
    "/products/{product_id}",
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
    "/products",
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
    "/products/{product_id}",
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
    "/products/{product_id}",
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
