from sqlmodel import SQLModel, Field
from pydantic import SecretStr, EmailStr, BaseModel



class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)

class LoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr

class TokenOut(BaseModel):
    access_token: str
    token_type: str
