from sqlmodel import SQLModel, Field
from app.modules.catalog.models import CategoryBase
import uuid
import uuid6


class Category(CategoryBase, table=True):
    category_id: uuid.UUID = Field(default_factory=uuid6.uuid7, primary_key=True)

