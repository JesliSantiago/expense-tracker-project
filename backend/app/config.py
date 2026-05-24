from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "ExpenseTracker"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str

    DATABASE_URL: str

    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ALLOWED_ORIGINS: str = "http://localhost:3000"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()
