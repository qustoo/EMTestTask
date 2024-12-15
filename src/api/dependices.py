from typing import Annotated

from fastapi import Depends

from schemas.filters import (AuthorFilterSchema, BookFilterSchema,
                             BorrowFilterSchema)
from services.author_service import AuthorService
from services.book_service import BookService
from services.borrow_service import BorrowService
from unit_of_works.librally_uow import LibraryUOW

# LibraryDep
LibraryUOWDep = Annotated[LibraryUOW, Depends(LibraryUOW)]

# Services
AuthorServiceDep = Annotated[AuthorService, Depends(AuthorService)]
BookServiceDep = Annotated[BookService, Depends(BookService)]
BorrowServiceDep = Annotated[BorrowService, Depends(BorrowService)]

# Filters
AuthorFilterDep = Annotated[AuthorFilterSchema, Depends(AuthorFilterSchema)]
BookFilterDep = Annotated[BookFilterSchema, Depends(BookFilterSchema)]
BorrowFilterDep = Annotated[BorrowFilterSchema, Depends(BorrowFilterSchema)]
