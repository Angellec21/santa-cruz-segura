from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "santa_cruz_segura"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DATABASE_URL: str | None = None  # override completo (Aiven lo provee)

    SECRET_KEY: str = "cambia_esto"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    APP_ENV: str = "development"
    UPLOAD_DIR: str = "uploads/"
    MAX_UPLOAD_MB: int = 10

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
