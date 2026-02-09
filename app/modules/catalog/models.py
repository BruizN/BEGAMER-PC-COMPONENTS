from sqlmodel import Field, Relationship
from app.core.AuditMixin import AuditMixin
from app.modules.catalog.schemas import CategoryBase, BrandBase, ProductBase
import uuid
import uuid6


class Category(CategoryBase, AuditMixin, table=True):
    category_id: uuid.UUID = Field(default_factory=uuid6.uuid7, primary_key=True)
    products: list["Product"] = Relationship(back_populates="category")

class Brand(BrandBase, AuditMixin, table=True):
    brand_id: uuid.UUID = Field(default_factory=uuid6.uuid7, primary_key=True)
    products: list["Product"] = Relationship(back_populates="brand")

class Product(ProductBase, AuditMixin, table=True):
    product_id: uuid.UUID = Field(default_factory=uuid6.uuid7, primary_key=True)
    slug: str = Field(unique=True, index=True)
    category_id: uuid.UUID = Field(foreign_key="category.category_id")
    brand_id: uuid.UUID = Field(foreign_key="brand.brand_id")
    category: "Category" = Relationship(back_populates="products")
    brand: "Brand" = Relationship(back_populates="products")