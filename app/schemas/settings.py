from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_password: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()