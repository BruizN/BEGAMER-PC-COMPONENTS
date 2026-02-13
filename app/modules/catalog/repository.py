from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
import uuid
from app.modules.catalog.models import Category, Brand, Product
from app.modules.catalog.exceptions import (
    CategoryAlreadyExistsError, 
    CategoryNotFoundError, 
    CategoryNotEmptyError,
    BrandAlreadyExistsError,
    BrandNotFoundError,
    BrandNotEmptyError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
    )

async def add_category(
    session: AsyncSession,
    new_category: Category
) -> Category:
    session.add(new_category)
    try:
        await session.flush()
    except IntegrityError as e:
        error_msg = str(e.orig) 
        # Duplicado por CODIGO
        if "code" in error_msg: 
             raise CategoryAlreadyExistsError(
                f"The category with the code '{new_category.code}' already exists."
             )
        # Duplicado por NOMBRE
        elif "name" in error_msg:
             raise CategoryAlreadyExistsError(
                f"The category with the name '{new_category.name}' already exists."
             )           
             
        raise e 
        
    return new_category

async def get_category(
    session: AsyncSession,
    category_id: uuid.UUID,
    only_active: bool
) -> Category:
    query = select(Category).where(Category.category_id == category_id)
    if only_active:
        query = query.where(Category.is_active)
    
    result = await session.exec(query)
    category = result.first()
    if not category:
        raise CategoryNotFoundError("Category not found")
    return category

async def get_all_categories(
    session: AsyncSession,
    offset: int,
    limit: int,
    only_active: bool = True
) -> list[Category]:
    query = select(Category)
    if only_active:
        query = query.where(Category.is_active)
    
    query = query.order_by(Category.created_at.desc())
    query = query.offset(offset).limit(limit)
    result = await session.exec(query)
    return list(result.all())

async def update_category(
    session: AsyncSession,
    category_id: uuid.UUID,
    update_data: dict
) -> Category:
    category = await session.get(Category, category_id)

    if not category:
        raise CategoryNotFoundError("Category not found")
        
    category.sqlmodel_update(update_data)
    
    session.add(category)
    try:
        await session.flush()
    except IntegrityError as e:
        error_msg = str(e.orig) 

        if "code" in error_msg: 
             raise CategoryAlreadyExistsError(
                f"The category with the code '{update_data["code"]}' already exists."
             )

        elif "name" in error_msg:
             raise CategoryAlreadyExistsError(
                f"The category with the name '{update_data["name"]}' already exists."
             )           
        raise e 
        
    await session.refresh(category)
    return category

async def remove_category(

    session: AsyncSession,

    category_id: uuid.UUID

) -> None:

    category = await session.get(Category, category_id)

    if not category:
        raise CategoryNotFoundError("Category not found")

    await session.delete(category)

    try:
        await session.flush()

    except IntegrityError as e:
        if "foreign key constraint" in str(e.orig):
            raise CategoryNotEmptyError("Cannot delete category: The category contains products. Please archive the category instead.")
        raise e

    return

async def add_brand(
    session: AsyncSession,
    new_brand: Brand
) -> Brand:
    session.add(new_brand)
    try:
        await session.flush()
    except IntegrityError as e:
        error_msg = str(e.orig) 

        if "code" in error_msg: 
             raise BrandAlreadyExistsError(
                f"The brand with the code '{new_brand.code}' already exists."
             )

        elif "name" in error_msg:
             raise BrandAlreadyExistsError(
                f"The brand with the name '{new_brand.name}' already exists."
             )           
             
        raise e 
    return new_brand

async def get_brand(
    session: AsyncSession,
    brand_id: uuid.UUID,
    only_active: bool
) -> Brand:
    query = select(Brand).where(Brand.brand_id == brand_id)
    if only_active:
        query = query.where(Brand.is_active)
    
    result = await session.exec(query)
    brand = result.first()
    if not brand:
        raise BrandNotFoundError("Brand not found")
    return brand

async def get_all_brands(
    session: AsyncSession,
    offset: int,
    limit: int,
    only_active: bool = True
) -> list[Brand]:
    query = select(Brand)
    if only_active:
        query = query.where(Brand.is_active)
    query = query.order_by(Brand.created_at.desc())
    query = query.offset(offset).limit(limit)
    result = await session.exec(query)
    return list(result.all())

async def update_brand(
    session: AsyncSession,
    brand_id: uuid.UUID,
    update_data: dict
) -> Brand:
    brand = await session.get(Brand, brand_id)

    if not brand:
        raise BrandNotFoundError("Brand not found")

    brand.sqlmodel_update(update_data)

    session.add(brand)
    try:
        await session.flush()
    except IntegrityError as e:
        error_msg = str(e.orig) 

        if "code" in error_msg: 
             raise BrandAlreadyExistsError(
                f"The brand with the code '{update_data["code"]}' already exists."
             )

        elif "name" in error_msg:
             raise BrandAlreadyExistsError(
                f"The brand with the name '{update_data["name"]}' already exists."
             )           
        raise e 
        
    await session.refresh(brand)
    return brand

async def remove_brand(
    session: AsyncSession,
    brand_id: uuid.UUID
) -> None:
    brand = await session.get(Brand, brand_id)

    if not brand:
        raise BrandNotFoundError("Brand not found")
    
    await session.delete(brand)

    try:
        await session.flush()

    except IntegrityError as e:
        if "foreign key constraint" in str(e.orig):
            raise BrandNotEmptyError(
                "Cannot delete brand: The brand contains products. Please archive the brand instead."
                )
        raise e

    return  

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
    only_active: bool = True,
    category_id: uuid.UUID | None = None,
    brand_id: uuid.UUID | None = None,
    search: str | None = None
) -> list[Product]:
    query = (
        select(Product)
        .options(
            joinedload(Product.brand),
            joinedload(Product.category)
        )
    )

    if only_active:
        query = query.where(Product.is_active)

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
            raise ProductNotEmptyError( # noqa: F821
                "Cannot delete product: The product contains variants associated. Please archive the product instead."
                )
        raise e

    return  
