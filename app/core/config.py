from pydantic_settings import BaseSettings
from os.path import join, dirname, abspath


WORK_DIR: str = dirname(dirname(dirname(abspath(__file__))))


class Settings(BaseSettings):
    API_KEY: str = "some_super_secret_api_key"
    DATABASE_URL: str
    MAX_ACTIVITY_DEPTH: int = 3

    class Config:
        env_file = join(WORK_DIR, ".env-dev")


settings = Settings()

# print(WORK_DIR)
# print(settings.Config.env_file)
# print(settings.DATABASE_URL)
