import uuid
from email.policy import default

from pydantic import Field

from schemas.base import BaseModel


class SuccessIdResponseSchema(BaseModel):
    """Схема ответа при успешном регистрации."""

    detail: str = Field(default=uuid.uuid4())


class SuccessCreatedItemResponse(BaseModel):
    """Схема ответа при успешном регистрации."""

    detail: str = Field(default="Ресурс успешно создан.")


class SuccessBoolResponseSchema(BaseModel):
    """Схема ответа при успешном выполнении операции."""

    detail: bool = Field(default=True)


class BadRequestResponseSchema(BaseModel):
    """Схема ответа при неправильном запросе."""

    detail: str = Field(default="Некорректные данные.")


class BookAlreadyBorrowedSchema(BaseModel):
    detail: str = Field(default="Книга уже забронированна другим читателем.")


class NotFoundResponseSchema(BaseModel):
    """Схема ответа при не найденном ресурсе."""

    detail: str = Field(default="Данные не найдены.")


class ServerErrorResponseSchema(BaseModel):
    detail: str = Field(default="Внутренняя ошибка сервера.")
