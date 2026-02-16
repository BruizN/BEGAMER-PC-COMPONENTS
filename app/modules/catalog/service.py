from app.modules.catalog.repository import category_repo as cat_repo
from app.modules.catalog.repository import brand_repo as brand_repo
from app.modules.catalog.repository import product_repo as prod_repo
from app.modules.catalog.models import Category, Brand, Product
from app.modules.catalog.schemas import (
    CategoryCreate, 
    CategoryUpdate,
    BrandCreate,
    BrandUpdate,
    ProductCreate,
    ProductUpdate
)
from sqlmodel.ext.asyncio.session import AsyncSession
from slugify import slugify
import uuid

async def create_category(
    session: AsyncSession,
    category_data: CategoryCreate
) -> Category:
    new_category = Category.model_validate(category_data)
    
    return await cat_repo.add_category(session, new_category)

async def get_category(
    session: AsyncSession,
    category_id: uuid.UUID,
    only_active: bool
) -> Category:
    return await cat_repo.get_category(session, category_id, only_active)
    
async def list_categories(
    session: AsyncSession,
    offset: int,
    limit: int,
    is_active: bool | None = True
) -> list[Category]:
    return await cat_repo.get_all_categories(session, offset, limit, is_active)

async def edit_category(
    session: AsyncSession,
    category_id: uuid.UUID,
    edit_category_data: CategoryUpdate 
) -> Category:
    update_data = edit_category_data.model_dump(exclude_unset=True)
    return await cat_repo.update_category(session, category_id, update_data)

async def delete_category(
    session: AsyncSession, 
    category_id: uuid.UUID
) -> None:
    await cat_repo.remove_category(session, category_id)
    return

async def create_brand(
    session: AsyncSession,
    brand_data: BrandCreate
) -> Brand:
    new_brand = Brand.model_validate(brand_data)

    return await brand_repo.add_brand(session, new_brand)

async def get_brand(
    session: AsyncSession,
    brand_id: uuid.UUID,
    only_active: bool
) -> Brand:
    return await brand_repo.get_brand(session, brand_id, only_active)

async def list_brands(
    session: AsyncSession,
    offset: int,
    limit: int,
    is_active: bool | None = True
) -> list[Brand]:
    return await brand_repo.get_all_brands(session, offset, limit, is_active)

async def edit_brand(
    session: AsyncSession,
    brand_id: uuid.UUID,
    edit_brand_data: BrandUpdate
) -> Brand:
    update_data = edit_brand_data.model_dump(exclude_unset=True)
    return await brand_repo.update_brand(session, brand_id, update_data)

async def delete_brand(
    session: AsyncSession,
    brand_id: uuid.UUID
) -> None:
    await brand_repo.remove_brand(session, brand_id)
    return 

async def create_product(
    session: AsyncSession,
    product_data: ProductCreate
) -> Product:
    brand = await get_brand(session, product_data.brand_id, True)
    category = await get_category(session, product_data.category_id, True)

    nombre_producto = product_data.name
    nombre_marca = brand.name

    # Si el nombre del producto ya empieza con la marca, no se agrega la marca de nuevo
    if nombre_producto.lower().startswith(nombre_marca.lower()):
        slug_text = f"{category.code} {nombre_producto}" 
    else:
        slug_text = f"{category.code} {nombre_marca} {nombre_producto}"

    generated_slug = slugify(slug_text)

    new_product = Product.model_validate(
        product_data,
        update={
            "slug": generated_slug
        }
    )
    return await prod_repo.add_product(session, new_product)

async def get_product(
    session: AsyncSession,
    product_id: uuid.UUID,
    only_active: bool
) -> Product:
    return await prod_repo.get_product(session, product_id, only_active)

async def list_products(
    session: AsyncSession,
    offset: int,
    limit: int,
    category_id: uuid.UUID | None = None,
    brand_id: uuid.UUID | None = None,
    search: str | None = None,
    is_active: bool | None = None
) -> list[Product]:
    return await prod_repo.get_all_products(session, offset, limit, category_id, brand_id, search, is_active)

async def edit_product(
    session: AsyncSession,
    product_id: uuid.UUID,
    edit_product_data: ProductUpdate
) -> Product:

    # Obtener el producto actual
    current_product = await prod_repo.get_product(session, product_id, False)

    update_data = edit_product_data.model_dump(exclude_unset=True)

    # Detectar si hay que recalcular el slug
    has_name_changed = "name" in update_data
    has_brand_changed = "brand_id" in update_data
    has_category_changed = "category_id" in update_data

    if has_name_changed or has_brand_changed or has_category_changed:
        
        # Resolver cual es el nombre definitivo
        effective_name = update_data.get("name", current_product.name)

        # Resolver cual es la marca definitiva (ID)
        effective_brand_id = update_data.get("brand_id", current_product.brand_id)
        effective_category_id = update_data.get("category_id", current_product.category_id)

        brand = await get_brand(session, effective_brand_id, False)
        category = await get_category(session, effective_category_id, False)
        
        brand_name_lower = brand.name.lower()
        product_name_lower = effective_name.lower()
        
        if product_name_lower.startswith(brand_name_lower):
            slug_text = f"{category.code} {effective_name}"
        else:
            slug_text = f"{category.code} {brand.name} {effective_name}"
            
        new_slug = slugify(slug_text)
        
        update_data["slug"] = new_slug

    return await prod_repo.update_product(session, product_id, update_data)


async def delete_product(
    session: AsyncSession,
    product_id: uuid.UUID
) -> None:
    await prod_repo.remove_product(session, product_id)
    return