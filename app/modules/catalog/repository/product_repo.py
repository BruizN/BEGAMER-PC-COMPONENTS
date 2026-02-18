from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
import uuid
from app.modules.catalog.models import Product
from app.modules.catalog.exceptions import (
    ProductAlreadyExistsError,
    ProductNotFoundError,
    ProductNotEmptyError
    )


async def add_product(
    session: AsyncSession,
    new_product: Product
) -> Product:
    session.add(new_product)
    try:
        await session.flush()
    except IntegrityError as e:
        error_msg = str(e.orig) 

        if "name" in error_msg: 
             raise ProductAlreadyExistsError(
                f"The product with the name '{new_product.name}' already exists."
             )

        elif "slug" in error_msg:
             raise ProductAlreadyExistsError(
                f"The product with the slug '{new_product.slug}' already exists."
             )           
             
        raise e 

    await session.refresh(new_product, ["category", "brand"])
    return new_product

async def get_product(
    session: AsyncSession,
    product_id: uuid.UUID,
    only_active: bool
) -> Product:
    query = (
        select(Product)
        .where(Product.product_id == product_id)
        .options(
            joinedload(Product.brand),
            joinedload(Product.category)
        )
    )

    if only_active:
        query = query.where(Product.is_active)
    
    result = await session.exec(query)
    product = result.first()
    if not product:
        raise ProductNotFoundError("Product not found")
    return product

async def get_all_products(
    session: AsyncSession,
    offset: int,
    limit: int,
    category_id: uuid.UUID | None = None,
    brand_id: uuid.UUID | None = None,
    search: str | None = None,
    is_active: bool | None = None
) -> list[Product]:
    query = (
        select(Product)
        .options(
            joinedload(Product.brand),
            joinedload(Product.category)
        )
    )

    if is_active is not None:
        query = query.where(Product.is_active == is_active)

    if category_id:
        query = query.where(Product.category_id == category_id)

    if brand_id:
        query = query.where(Product.brand_id == brand_id)

    if search:
        query = query.where(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
        )

    query = query.order_by(Product.created_at.desc())
    query = query.offset(offset).limit(limit)
    
    result = await session.exec(query)
    return list(result.unique().all())

async def update_product(
    session: AsyncSession,
    product_id: uuid.UUID,
    update_data: dict
) -> Product:
    product = await session.get(Product, product_id)

    if not product:
        raise ProductNotFoundError("Product not found")

    product.sqlmodel_update(update_data)

    session.add(product)
    try:
        await session.flush()
    except IntegrityError as e:
        error_msg = str(e.orig) 

        if "name" in error_msg: 
             raise ProductAlreadyExistsError(
                f"The product with the name '{update_data["name"]}' already exists."
             )

        elif "slug" in error_msg:
             raise ProductAlreadyExistsError(
                f"The product with the slug '{update_data["slug"]}' already exists."
             )           
             
        raise e 

    await session.refresh(product, ["category", "brand", "updated_at"])
    return product


async def remove_product(
    session: AsyncSession,
    product_id: uuid.UUID
) -> None:
    product = await session.get(Product, product_id)

    if not product:
        raise ProductNotFoundError("Product not found")
    
    await session.delete(product)

    try:
        await session.flush()

    except IntegrityError as e:
        if "foreign key constraint" in str(e.orig):
            raise ProductNotEmptyError(
                "Cannot delete product: The product contains variants associated. Please archive the product instead."
                )
        raise e

    return  
