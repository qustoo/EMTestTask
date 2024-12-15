from datetime import date
from uuid import UUID

from pydantic import Field, field_validator

from exceptions.exceptions_classes import BadRequestException
from schemas.base import BaseModel


class AuthorBaseSchema(BaseModel):
    first_name: str
    last_name: str
    birth_date: date

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, first_name: str) -> str:
        if first_name and len(first_name) < 3 or len(first_name) > 50:
            raise BadRequestException(
                detail="Символов в имени должно быть не меньше чем 3 или больше чем 50 символов."
            )
        return first_name

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, last_name: str) -> str:
        if last_name and len(last_name) < 3:
            raise BadRequestException(
                detail="Символов в фамилии должно быть не меньше чем 3."
            )
        return last_name

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, birth_date: date) -> date:
        current_year = date.today().year
        if birth_date and birth_date.year < 1900:
            raise BadRequestException(detail="Год рождения не может быть раньше 1900.")
        if current_year - birth_date.year > 125:
            raise BadRequestException(
                detail="Возраст автора не может превышать 125 лет."
            )
        return birth_date


class AuthorResponseSchema(AuthorBaseSchema):
    id: UUID


class AuthorRegisterSchema(AuthorBaseSchema):
    first_name: str = Field(default="Ivan")
    last_name: str = Field(default="Ivanov")
    birth_date: date = Field(default_factory=date.today)


class AuthorUpdateSchema(AuthorBaseSchema):
    first_name: str = Field(default="updatedIvan")
    last_name: str = Field(default="updated Ivanov")
    birth_date: date = Field(default_factory=date.today)
