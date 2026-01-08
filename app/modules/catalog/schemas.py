from sqlmodel import SQLModel, Field
import uuid


class CategoryBase(SQLModel):
    name: str = Field(unique=True, index=True)

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    category_id: uuid.UUID

class CategoryUpdate(CategoryBase):
    pass

class BrandBase(SQLModel):
    name: str = Field(unique=True, index=True)

class BrandCreate(BrandBase):
    pass

class BrandRead(BrandBase):
    brand_id: uuid.UUID

class BrandUpdate(BrandBase):
    pass