from sqlmodel import Field, Relationship
from app.core.AuditMixin import AuditMixin
from app.modules.catalog.schemas import CategoryBase, BrandBase, ProductBase
import uuid
import uuid6


class Category(CategoryBase, AuditMixin, table=True):
    name: str = Field(unique=True, index=True)
    code: str = Field(unique=True, index=True)
    category_id: uuid.UUID = Field(default_factory=uuid6.uuid7, primary_key=True)
    products: list["Product"] = Relationship(back_populates="category", passive_deletes=True)

class Brand(BrandBase, AuditMixin, table=True):
    name: str = Field(unique=True, index=True)
    code: str = Field(unique=True, index=True)
    brand_id: uuid.UUID = Field(default_factory=uuid6.uuid7, primary_key=True)
    products: list["Product"] = Relationship(back_populates="brand", passive_deletes=True) #evita la actualizacion de hijos a none al eliminar el padre

class Product(ProductBase, AuditMixin, table=True):
    product_id: uuid.UUID = Field(default_factory=uuid6.uuid7, primary_key=True)
    name: str = Field(unique=True, index=True)
    slug: str = Field(unique=True, index=True)
    category_id: uuid.UUID = Field(foreign_key="category.category_id")
    brand_id: uuid.UUID = Field(foreign_key="brand.brand_id")
    category: "Category" = Relationship(back_populates="products")
    brand: "Brand" = Relationship(back_populates="products")