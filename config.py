from confluent_kafka import Producer
from pydantic_settings import BaseSettings, SettingsConfigDict

kafka_producer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}
producer = Producer(kafka_producer_config)


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    model_config = SettingsConfigDict(env_file='.env')

    @property
    def get_db_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.DB_USER}:'
            f'{self.DB_PASSWORD}@{self.DB_HOST}:'
            f'{self.DB_PORT}/{self.DB_NAME}'
        )
