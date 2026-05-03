from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_TO: str

    class Config:
        env_file = ".env"

settings = Settings()