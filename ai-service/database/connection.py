import os
from typing import AsyncGenerator, Optional

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class DatabaseManager:
    _instance: Optional["DatabaseManager"] = None
    _async_engine: Optional[AsyncEngine] = None
    _sync_engine = None

    def __new__(cls) -> "DatabaseManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True
        self.async_database_url = os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://postgres:postgres@localhost:5432/exam_assistant_db",
        )
        self.sync_database_url = os.getenv(
            "DATABASE_SYNC_URL",
            "postgresql://postgres:postgres@localhost:5432/exam_assistant_db",
        )
        self.pool_size = int(os.getenv("DB_POOL_SIZE", "10"))
        self.max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "20"))
        self._async_session_factory: Optional[async_sessionmaker] = None
        self._sync_session_factory: Optional[sessionmaker] = None

    async def initialize(self) -> None:
        if self._async_engine is not None:
            return
        logger.info("Initializing database connections...")
        self._async_engine = create_async_engine(
            self.async_database_url,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_pre_ping=True,
            echo=False,
        )
        self._async_session_factory = async_sessionmaker(
            self._async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self._sync_engine = create_engine(
            self.sync_database_url,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_pre_ping=True,
            echo=False,
        )
        self._sync_session_factory = sessionmaker(
            bind=self._sync_engine,
            expire_on_commit=False,
        )

        try:
            async with self._async_engine.connect() as conn:
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                await conn.commit()
            logger.info("pgvector extension verified")
        except Exception as e:
            logger.warning(f"Could not create vector extension: {e}")

        logger.info("Database connections initialized successfully")

    async def close(self) -> None:
        if self._async_engine:
            await self._async_engine.dispose()
            logger.info("Async database engine disposed")
        if self._sync_engine:
            self._sync_engine.dispose()
            logger.info("Sync database engine disposed")

    def get_async_session_factory(self) -> async_sessionmaker:
        if self._async_session_factory is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._async_session_factory

    def get_sync_session_factory(self) -> sessionmaker:
        if self._sync_session_factory is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._sync_session_factory

    @property
    def async_engine(self) -> AsyncEngine:
        if self._async_engine is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._async_engine

    @property
    def sync_engine(self):
        if self._sync_engine is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._sync_engine


db_manager = DatabaseManager()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    factory = db_manager.get_async_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_connection():
    factory = db_manager.get_sync_session_factory()
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
