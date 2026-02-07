from sqlmodel import SQLModel, Field
from pydantic import field_validator
from datetime import datetime
import uuid
import re


class HasCodeMixin(SQLModel):
    code: str = Field(unique=True, index=True, min_length=2, max_length=4)

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str | None) -> str | None:
        # Si es None (en un PATCH), retornasin validar
        if v is None:
            return v
            
        v = v.upper().strip()
        if not (2 <= len(v) <= 4):
            raise ValueError("The code must be between 2 and 4 characters long.")
        if not re.match("^[A-Z0-9]+$", v):
            raise ValueError("The code can only contain letters and numbers.")
        return v

class HasNameMixin(SQLModel):
    name: str = Field(unique=True, index=True, min_length=3, max_length=30)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is None:
            return v
            
        v = v.title().strip()
        if not (3 <= len(v) <= 30):
            raise ValueError("The name must be between 3 and 30 characters long.")

        return v


class CategoryBase(HasNameMixin, HasCodeMixin, SQLModel):
    pass

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    category_id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

class CategoryUpdate(HasNameMixin, HasCodeMixin, SQLModel):
    # Sobrescribe los campos para hacerlos opcionales.
    name: str | None = Field(default=None, min_length=3, max_length=30)
    code: str | None = Field(default=None, min_length=2, max_length=4)
    is_active: bool | None = None

class BrandBase(HasNameMixin, HasCodeMixin, SQLModel):
    pass

class BrandCreate(BrandBase):
    pass

class BrandRead(BrandBase):
    brand_id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

class BrandUpdate(HasNameMixin, HasCodeMixin, SQLModel):
    name: str | None = Field(default=None, min_length=3, max_length=30)
    code: str | None = Field(default=None, min_length=2, max_length=4)
    is_active: bool | None = None