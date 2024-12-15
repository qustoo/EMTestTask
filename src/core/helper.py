from functools import lru_cache

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from core.config import settings


def _build_tools() -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(
        url=settings.db.async_db_url,
        echo=settings.helper.echo,
        echo_pool=settings.helper.echo_pool,
        pool_size=settings.helper.pool_size,
        max_overflow=settings.helper.max_overflow,
    )
    session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    return engine, session_factory


class DatabaseHelper:
    def __init__(self) -> None:
        self.engine, self.session_factory = _build_tools()


@lru_cache
def get_helper() -> DatabaseHelper:
    return DatabaseHelper()


helper = get_helper()
