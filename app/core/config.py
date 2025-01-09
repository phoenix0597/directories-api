from pydantic_settings import BaseSettings
from os.path import join, dirname, abspath


WORK_DIR: str = dirname(dirname(dirname(abspath(__file__))))


class Settings(BaseSettings):
    API_KEY: str
    DATABASE_URL: str
    MAX_ACTIVITY_DEPTH: int = 3
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    GEOALCHEMY_TABLES_FILE: str = join(WORK_DIR, "alembic", "geoalchemy_tables.txt")

    class Config:
        env_file = join(WORK_DIR, ".env-dev")


settings = Settings()

# print(WORK_DIR)
# print(settings.Config.env_file)
# print(settings.DATABASE_URL)
