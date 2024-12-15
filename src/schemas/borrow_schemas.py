from datetime import date
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from exceptions.exceptions_classes import BadRequestException
from schemas.base import BaseModel


class BorrowBaseSchema(BaseModel):
    book_id: UUID
    reader_name: str
    borrow_date: date

    @field_validator("reader_name")
    @classmethod
    def validate_first_name(cls, reader_name: str) -> str:
        if len(reader_name) < 3 or len(reader_name) > 50:
            raise BadRequestException(
                detail="Символов в имени читателя должно быть не меньше чем 3 или больше чем 50 символов."
            )
        return reader_name


class BorrowResponseSchema(BorrowBaseSchema):
    id: UUID


class BorrowRegisterSchema(BorrowBaseSchema):
    reader_name: str = Field(default="Reader name")
    book_id: UUID = Field(default_factory=UUID)
    borrow_date: date = Field(default_factory=date.today)


class BorrowUpdateSchema(BorrowBaseSchema):
    pass


class BorrowedReturnSchema(BaseModel):
    book_id: UUID = Field(default_factory=UUID)
    return_date: date = Field(default_factory=date.today)
