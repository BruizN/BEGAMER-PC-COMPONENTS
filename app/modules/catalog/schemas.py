from sqlmodel import SQLModel, Field


class CategoryBase(SQLModel):
    name: str = Field(unique=True, index=True)

