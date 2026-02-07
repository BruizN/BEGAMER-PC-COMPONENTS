from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import func, DateTime

class AuditMixin(SQLModel):
    created_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),    
        sa_column_kwargs={
            "server_default": func.now()
        }
    )

    updated_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now()
        }
    )
    is_active: bool = True