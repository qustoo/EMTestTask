from types import TracebackType
from typing import Optional

from typing_extensions import Self

from repositories.author_repository import AuthorRepository
from repositories.book_repository import BookRepository
from repositories.borrow_repository import BorrowRepository
from unit_of_works.base import BaseUnitOfWork


class LibraryUOW(BaseUnitOfWork):
    async def __aenter__(self) -> Self:
        """Метод входа в контекстного менеджера для автора."""
        await super().__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Выход из контекстного менеджера для автора."""
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.close()

    @property
    def books(self):
        return BookRepository(self._session)

    @property
    def borrows(self):
        return BorrowRepository(self._session)

    @property
    def authors(self):
        return AuthorRepository(self._session)
