from typing import Optional
from uuid import UUID

from pydantic import Field, field_validator

from exceptions.exceptions_classes import BadRequestException
from schemas.base import BaseModel


class BookBaseSchema(BaseModel):
    title: str
    description: str
    count: int
    author_id: UUID

    @field_validator("title")
    @classmethod
    def validate_title(cls, title: str) -> str:
        if len(title) < 1 or len(title) > 100:
            raise BadRequestException(
                detail="Название не может быть меньше 1 и/или больше 100 символов."
            )
        return title

    @field_validator("description")
    @classmethod
    def validate_description(cls, description: str) -> str:
        if len(description) < 1 or len(description) > 250:
            raise BadRequestException(
                detail="Описание не может быть меньше 1 и/или больше 250 символов."
            )
        return description

    @field_validator("count")
    @classmethod
    def validate_count(cls, count: int) -> int:
        if count < 0:
            raise BadRequestException(
                detail="Количество книг не может быть отрицательным."
            )
        return count


class BookResponseSchema(BookBaseSchema):
    id: UUID


class BookRegisterSchema(BookBaseSchema):
    title: str = Field(default="book title")
    description: str = Field(default="book description")
    count: int = Field(default=1)
    author_id: UUID


class BookUpdateSchema(BookBaseSchema):
    title: Optional[str] = Field(default="updated title")
    description: Optional[str] = Field(default="updated description")
    count: Optional[int] = Field(default=1)
