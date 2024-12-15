import abc
from typing import TypeVar

from repositories.base import BaseRepository

TypeRepository = TypeVar("TypeRepository", bound=BaseRepository)


class AbstractUnitOfWork(abc.ABC):
    """Абстрактный класс для работы с транзакциями."""

    @abc.abstractmethod
    def __init__(self) -> None: ...

    @abc.abstractmethod
    async def __aenter__(self) -> TypeRepository:
        """Абстрактный метод входа в контекстного менеджера."""

    @abc.abstractmethod
    async def __aexit__(self, *args) -> None:
        """Абстрактный метод выхода из контекстного менеджера"""

    @abc.abstractmethod
    async def commit(self) -> None:
        """Абстрактный метод фиксирования транзакции."""

    @abc.abstractmethod
    async def rollback(self) -> None:
        """Абстрактный метод завершения транзакции."""
