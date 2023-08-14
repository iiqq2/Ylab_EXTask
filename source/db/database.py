from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)
session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


metadata = MetaData()


async def get_db() -> AsyncGenerator:
    db = session()
    try:
        yield db
    finally:
        await db.close()
