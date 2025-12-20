from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_db: str
    postgres_port: int
    origins: list[str]
    secret_key: str
    broker_host: str
    broker_port: int

    @property
    def database_url(self) -> str:
        """Url for connecting to database"""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def broker_url(self) -> str:
        """Url for connecting to broker"""
        return f"{self.broker_host}:{self.broker_port}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
