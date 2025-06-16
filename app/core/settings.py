from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # models related
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    ORIGINS: list[str]

    SECRET_KEY: str

    @property
    def DATABASE_URL(self) -> str:
        """Url for connecting to models"""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
