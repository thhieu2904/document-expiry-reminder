"""
Async database engine and session management for Supabase PostgreSQL.
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.core.config import settings


# Use NullPool for transaction pooler (Supabase pgBouncer)
# This avoids conflicts with external connection pooling
engine = create_async_engine(
    settings.database_url,
    poolclass=NullPool,
    echo=settings.app_env == "development",
    connect_args={
        "prepared_statement_cache_size": 0,
        "statement_cache_size": 0
    },
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


async def get_db() -> AsyncSession:
    """FastAPI dependency: yield an async database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
