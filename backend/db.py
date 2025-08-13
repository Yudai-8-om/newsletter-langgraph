import asyncio
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.settings import settings
from contextlib import asynccontextmanager

if settings.DEPLOY_LOCATION == "remote":
    engine = create_async_engine(settings.DATABASE_URL_SUPABASE, echo=True, pool_size=5, max_overflow=10, pool_pre_ping=True, pool_recycle=240)
else:
    engine = create_async_engine(settings.DATABASE_URL_NO_DOCKER, echo=True, pool_size=5, max_overflow=10)
    
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False) 

# Function to get a PostgreSQL database session
@asynccontextmanager
async def get_pg_async_session():
    """
    Gets a PostgreSQL database async session.
    """
    async with AsyncSessionFactory() as session:
        yield session

#workaround for fastapi dependency
# https://github.com/fastapi/fastapi/discussions/8955

async def fastapi_async_session_dependency():
    """
    FastAPI async session dependency.
    """
    async with get_pg_async_session() as session:
        yield session