from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_url: str

    jwt_secret: str = Field(alias="SECRET_KEY")
    jwt_alg: str = Field(default="HS256", alias="ALGORITHM")
    jwt_expire_min: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore" 
    )

settings = Settings()