from types import TracebackType
from typing import Optional, TypeVar

from fastapi import HTTPException
from typing_extensions import Self

from core.helper import helper
from interfaces.abstraction_unit_of_work import AbstractUnitOfWork
from repositories.base import BaseRepository

TypeRepository = TypeVar("TypeRepository", bound=BaseRepository)


class BaseUnitOfWork(AbstractUnitOfWork):
    """Базовый класс для работы с транзакциями."""

    def __init__(self) -> None:
        self.__session_factory = helper.session_factory

    async def __aenter__(self) -> Self:
        """Базовый метод входа в контекстного менеджера."""
        self._session = self.__session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Базовый метод выхода из контекстного менеджера"""
        # Регистрируем и вызываем все кастомные исключения.
        if exc_type is not None and exc_type.__base__ == HTTPException:
            await self.rollback()
            await self.close()
            raise exc_val

        #  Регистрируем и вызываем не отслеживаемые исключения.
        if exc_type:
            await self.rollback()
            detail_massage = (
                getattr(exc_val, "detail")
                if getattr(exc_val, "detail", None)
                else exc_val.args[0] if exc_val.args else None
            )
            await self.close()
            raise HTTPException(status_code=500, detail=detail_massage)

    async def commit(self) -> None:
        """Базовый метод фиксирования транзакции."""
        await self._session.commit()

    async def rollback(self) -> None:
        """Базовый метод отмены транзакции."""
        await self._session.rollback()

    async def close(self) -> None:
        """Базовый метод закрытия транзакции."""
        await self._session.close()
