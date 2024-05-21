from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # FastAPI
    APP_NAME: str
    VERSION: str = "1.0"
    HOST: str
    PORT: int
    RELOAD: bool = False

    # Database
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
