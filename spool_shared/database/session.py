"""Database session management."""

from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
import structlog

logger = structlog.get_logger()


class DatabaseSession:
    """Database session manager."""
    
    def __init__(self, database_url: str, **engine_kwargs):
        """Initialize database session manager.
        
        Args:
            database_url: Database connection URL
            **engine_kwargs: Additional engine configuration
        """
        self.engine = create_async_engine(
            database_url,
            echo=engine_kwargs.get("echo", False),
            pool_pre_ping=engine_kwargs.get("pool_pre_ping", True),
            pool_size=engine_kwargs.get("pool_size", 5),
            max_overflow=engine_kwargs.get("max_overflow", 10),
            **{k: v for k, v in engine_kwargs.items() 
               if k not in ["echo", "pool_pre_ping", "pool_size", "max_overflow"]}
        )
        
        self.async_session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session.
        
        Yields:
            Database session
        """
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    @asynccontextmanager
    async def session_scope(self):
        """Session context manager.
        
        Usage:
            async with db.session_scope() as session:
                # Use session
        """
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                logger.error("Database session error", error=str(e))
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def close(self):
        """Close database connections."""
        await self.engine.dispose()


# Global session manager instance
_db_session: Optional[DatabaseSession] = None


def init_database(database_url: str, **kwargs) -> DatabaseSession:
    """Initialize global database session.
    
    Args:
        database_url: Database connection URL
        **kwargs: Additional configuration
        
    Returns:
        Database session manager
    """
    global _db_session
    _db_session = DatabaseSession(database_url, **kwargs)
    return _db_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session from global manager.
    
    Yields:
        Database session
        
    Raises:
        RuntimeError: If database not initialized
    """
    if _db_session is None:
        raise RuntimeError("Database not initialized. Call init_database first.")
    
    async for session in _db_session.get_session():
        yield session