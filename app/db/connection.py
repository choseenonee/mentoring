from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from .models import Base


def make_async_db_url(host: str, port: int, user: str, password: str, database: str) -> str:
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

def create_engine(db_url: str) -> AsyncEngine:
    return create_async_engine(db_url)

async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def create_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)
