import asyncio
import json
from datetime import date
from typing import AsyncGenerator, Generator

import asyncpg
import pytest
from httpx import ASGITransport, AsyncClient
from pytest import MonkeyPatch
from sqlalchemy import URL, Engine
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import close_all_sessions
from sqlalchemy.pool import NullPool

from core.config import settings
from core.helper import helper
from models.base import Base
from server import app as _app


@pytest.fixture(scope="session")
def monkeypatch_session() -> Generator[MonkeyPatch, None, None]:
    """Имитирование объекта MonkeyPatch для тестовых сессий."""
    monkeypatch = MonkeyPatch()
    try:
        yield monkeypatch
    finally:
        monkeypatch.undo()


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def __mock_db_url(monkeypatch_session: MonkeyPatch) -> None:
    async_db_url: URL = settings.db.async_db_url
    monkeypatch_session.setattr(
        target=settings.db,
        name="async_db_url",
        value=async_db_url.set(database="test"),
    )
    monkeypatch_session.setenv(name="db_name", value="test")
    monkeypatch_session.setattr(target=settings.db, name="db_name", value="test")


@pytest.fixture(scope="session", autouse=True)
async def __create_database(__mock_db_url) -> None:
    db_url = (
        f"postgresql://{settings.db.db_user}:{settings.db.db_password}@"
        f"{settings.db.db_host}:{settings.db.db_port}"
    )

    conn = await asyncpg.connect(db_url)
    try:
        await conn.execute(f"DROP DATABASE IF EXISTS {settings.db.db_name};")
        await conn.execute(f"CREATE DATABASE {settings.db.db_name};")
    finally:
        await conn.close()

    yield

    conn = await asyncpg.connect(db_url)
    try:
        await conn.execute(f"DROP DATABASE IF EXISTS {settings.db.db_name};")
    finally:
        await conn.close()


@pytest.fixture(scope="session", autouse=True)
def __mock_sessions_factories(
    async_db_engine: AsyncEngine,
) -> None:
    """
    Имитирует 'engine_async' из 'core.helper'.
    """
    helper.session_factory.configure(bind=async_db_engine)


@pytest.fixture(scope="session")
async def async_db_engine() -> Generator[Engine, None, None]:
    """Создание асинхронного SQLAlchemy Engine."""
    async_engine = create_async_engine(settings.db.async_db_url, poolclass=NullPool)
    try:
        yield async_engine
    finally:
        close_all_sessions()
        await async_engine.dispose()


@pytest.fixture(scope="session")
async def async_session_factory(
    async_db_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """Создание асинхронной фабрики сессий."""
    return async_sessionmaker(async_db_engine)


@pytest.fixture(scope="session")
async def async_client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=_app), base_url="http://localhost:8000/api/v1"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def async_session(async_db_engine, async_session_factory) -> AsyncGenerator:
    async with async_session_factory() as session:
        async with async_db_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield session


@pytest.fixture(scope="session", autouse=True)
async def drop_tables_after_all_tests(async_db_engine: AsyncEngine) -> None:
    """Удаление всех таблиц после завершения тестовой сессии."""
    yield

    # Удаление всех таблиц после тестов
    async with async_db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session", autouse=True)
async def set_up_data(async_client: AsyncClient):
    async def create_entity(url: str, data: dict) -> dict:
        response = await async_client.post(url, content=json.dumps(data))
        response.raise_for_status()  # Ensure the request was successful
        return response.json()

    author_data = {
        "first_name": "Test Firstname For Author",
        "last_name": "Test LastName For Author",
        "birth_date": date.today().isoformat(),
    }
    author = await create_entity("/authors/", author_data)

    book_data = {
        "title": "Book title",
        "description": "Book description",
        "count": 10,
        "author_id": author["id"],  # Use the created author's ID
    }
    book = await create_entity("/books/", book_data)

    # Fixture for creating a borrow record
    borrow_data = {
        "reader_name": "Ivanov",
        "book_id": book["id"],
        "borrow_date": date.today().isoformat(),
    }
    borrow = await create_entity("/borrows/", borrow_data)

    return {"author": author, "book": book, "borrow": borrow}


@pytest.fixture(scope="session")
def edit_author_data():
    return {
        "first_name": "Edit Test Firstname For Author",
        "last_name": "Edit Test LastName For Author",
        "birth_date": date.today().isoformat(),
    }


@pytest.fixture(scope="session")
def author_data():
    return {
        "first_name": "Test Firstname For Author",
        "last_name": "Test LastName For Author",
        "birth_date": date.today().isoformat(),
    }


@pytest.fixture(scope="session")
def book_data(set_up_data):
    return {
        "title": "Book title",
        "description": "Book description",
        "count": 10,
        "author_id": set_up_data["author"]["id"],
    }


@pytest.fixture(scope="session")
def edit_book_data(set_up_data):
    return {
        "title": "Edit Book title",
        "description": "Edit Book description",
        "count": 10,
        "author_id": set_up_data["author"]["id"],
    }


@pytest.fixture(scope="session")
def borrow_data(set_up_data):
    return {
        "reader_name": "Ivanov",
        "book_id": set_up_data["book"]["id"],
        "borrow_date": date.today().isoformat(),
    }
