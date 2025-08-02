import asyncio
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.settings import settings
from contextlib import asynccontextmanager


engine = create_async_engine(settings.DATABASE_URL_NO_DOCKER, echo=True, pool_size=5, max_overflow=10)
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False) 

@asynccontextmanager
async def get_pg_async_session():
    """
    Gets a PostgreSQL database async session.
    """
    async with AsyncSessionFactory() as session:
        yield session