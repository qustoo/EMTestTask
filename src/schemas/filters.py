from datetime import date
from typing import Optional

from pydantic import Field

from schemas.base import BaseModel


class BaseFilterSchema(BaseModel):
    limit: int = Field(default=100)
    offset: int = Field(default=0)


class AuthorFilterSchema(BaseFilterSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class BookFilterSchema(BaseFilterSchema):
    count: Optional[int] = None


class BorrowFilterSchema(BaseFilterSchema):
    return_date: Optional[date] = None
