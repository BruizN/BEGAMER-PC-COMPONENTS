from sqlmodel import SQLModel, Field
from app.core.types import CleanText, CleanCode
from datetime import datetime
import uuid
from decimal import Decimal

class CategoryBase(SQLModel):
    name: CleanText = Field(min_length=3, max_length=50)
    code: CleanCode = Field(min_length=2, max_length=4)

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    category_id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

class CategoryUpdate(SQLModel):
    # Sobrescribe los campos para hacerlos opcionales.
    name: CleanText | None = Field(default=None, min_length=3, max_length=50)
    code: CleanCode | None = Field(default=None, min_length=2, max_length=4)
    is_active: bool | None = None

class BrandBase(SQLModel):
    name: CleanText = Field(min_length=3, max_length=50)
    code: CleanCode = Field(min_length=2, max_length=4)

class BrandCreate(BrandBase):
    pass

class BrandRead(BrandBase):
    brand_id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

class BrandUpdate(SQLModel):
    name: CleanText | None = Field(default=None, min_length=3, max_length=50)
    code: CleanCode | None = Field(default=None, min_length=2, max_length=4)
    is_active: bool | None = None


class ProductBase(SQLModel):
    name: CleanText = Field(min_length=3, max_length=150)
    description: str | None = None
    category_id: uuid.UUID 
    brand_id: uuid.UUID

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    product_id: uuid.UUID
    slug: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    category: CategoryRead
    brand: BrandRead

class ProductUpdate(SQLModel):
    name: CleanText | None = Field(default=None, min_length=3, max_length=150)
    description: CleanText | None = None
    category_id: uuid.UUID | None = None
    brand_id: uuid.UUID | None = None
    is_active: bool | None = None


class ProductVariantBase(SQLModel):
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock: int = Field(ge=0)
    attributes: CleanText

class ProductVariantCreate(ProductVariantBase):
    pass


class ProductVariantUpdate(SQLModel):
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    stock: int | None = Field(default=None, ge=0)
    attributes: CleanText | None = None
    is_active: bool | None = None


# --- Esquemas de lectura ligera para variantes ---
class BrandBasic(SQLModel):
    name: str
    code: str

class CategoryBasic(SQLModel):
    name: str
    code: str

class ProductBasic(SQLModel):
    product_id: uuid.UUID
    name: str
    slug: str
    category: CategoryBasic 
    brand: BrandBasic

class ProductVariantRead(ProductVariantBase):
    variant_id: uuid.UUID
    sku: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    product: ProductBasic