from sqlmodel import SQLModel, Field
from app.core.types import CleanText, CleanCode
from datetime import datetime
import uuid

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