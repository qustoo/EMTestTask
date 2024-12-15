from typing import List

from sqlalchemy import UUID, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.mixins import CreatedUpdatedMixin, UUIDMixin


class Book(Base, CreatedUpdatedMixin, UUIDMixin):
    __table_args__ = (CheckConstraint("count >= 0", name="check_count_non_negative"),)

    title: Mapped[str] = mapped_column(String(length=100), nullable=False)
    description: Mapped[str] = mapped_column(String(length=100), nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("author.id"), nullable=False)

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    borrows: Mapped[List["Borrow"]] = relationship("Borrow", back_populates="book")
