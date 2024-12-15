from datetime import date

from sqlalchemy import UUID, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.mixins import CreatedUpdatedMixin, UUIDMixin


class Borrow(Base, CreatedUpdatedMixin, UUIDMixin):
    reader_name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    book_id: Mapped[UUID] = mapped_column(ForeignKey("book.id"), nullable=False)
    borrow_date: Mapped[date] = mapped_column(Date, nullable=False)
    return_date: Mapped[date] = mapped_column(Date, nullable=True)

    book = relationship("Book", back_populates="borrows")
