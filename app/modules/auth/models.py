from app.modules.auth.schemas import UserBase
from enum import Enum 
from sqlmodel import Field, AutoString
import uuid
import uuid6

class Role(str, Enum):
    ADMIN = "admin"
    CLIENT = "cliente"

class User(UserBase, table=True):
    user_id: uuid.UUID = Field(default_factory=uuid6.uuid7, primary_key=True)
    role: Role = Field(sa_type=AutoString) #Guarda el enum como String para evitar problemas de migraciones con PostgreSQL
    hashed_password: str
    is_active: bool = True