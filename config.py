from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_HOST: str
    TEST_DB_PORT: str
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()

DB_NAME = settings.DB_NAME
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD
DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT
TEST_DB_NAME = settings.TEST_DB_NAME
TEST_DB_USER = settings.TEST_DB_USER
TEST_DB_PASSWORD = settings.TEST_DB_PASSWORD
TEST_DB_HOST = settings.TEST_DB_HOST
TEST_DB_PORT = settings.TEST_DB_PORT