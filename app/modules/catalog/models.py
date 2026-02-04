from sqlmodel import Field
from app.core.AuditMixin import AuditMixin
from app.modules.catalog.schemas import CategoryBase, BrandBase
import uuid
import uuid6


class Category(CategoryBase, AuditMixin, table=True):
    category_id: uuid.UUID = Field(default_factory=uuid6.uuid7, primary_key=True)

class Brand(BrandBase, AuditMixin, table=True):
    brand_id: uuid.UUID = Field(default_factory=uuid6.uuid7, primary_key=True)