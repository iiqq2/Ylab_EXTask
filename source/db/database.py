from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import Settings

s = Settings()
DATABASE_URL = s.get_db_url

engine = create_async_engine(DATABASE_URL, echo=True)
session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db() -> AsyncGenerator:
    db = session()
    try:
        yield db
    finally:
        await db.close()
