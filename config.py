from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MAX_CHAR:int = 10000


settings = Settings()