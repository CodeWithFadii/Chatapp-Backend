from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expires_days: int

    postgres_user: str
    postgres_password: str
    postgres_db: str

    class Config:
        env_file = ".env"


settings = Settings() # type: ignore
