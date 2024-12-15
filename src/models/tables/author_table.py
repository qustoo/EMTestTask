from datetime import date
from typing import List

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.mixins import CreatedUpdatedMixin, UUIDMixin
from models.tables.book_table import Book


class Author(Base, CreatedUpdatedMixin, UUIDMixin):
    first_name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)

    books: Mapped[List["Book"]] = relationship("Book", back_populates="author")
