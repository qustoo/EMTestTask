from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional, TypeAlias, TypeVar, Union
from uuid import UUID

from models.base import Base
from schemas.base import BaseModel
from schemas.filters import BaseFilterSchema

TypeModel = TypeVar("TypeModel", bound=Base)
TypeSchema = TypeVar("TypeSchema", bound=BaseModel)
TypeFilter = TypeVar("TypeFilter", bound=BaseFilterSchema)

RegisterData: TypeAlias = dict[str, Union[str, date, bool, None]]
EditData: TypeAlias = dict[str, Union[UUID, str, bool, date, int, None]]
GetData: TypeAlias = dict[str, Union[str, date, bool, None]]
TypeID = TypeVar("TypeID", int, UUID)


class AbstractRepository(ABC):
    """Абстрактная класс репозитория."""

    model: type[TypeModel]

    @abstractmethod
    async def add(self, data: RegisterData) -> TypeID:
        """Абстрактный метод репозитория для добавления данных."""

    @abstractmethod
    async def get(self, **kwargs: GetData) -> Optional[TypeModel]:
        """Абстрактный метод репозитория для получения данных."""

    @abstractmethod
    async def get_all(self, filters) -> Optional[List[TypeModel]]:
        """Абстрактный метод репозитория для получения списка данных."""

    @abstractmethod
    async def edit(self, obj_id: TypeID, data: EditData) -> bool:
        """Абстрактный метод репозитория для редактирования данных."""

    @abstractmethod
    async def delete(self, obj_id: TypeID) -> bool:
        """Абстрактный метод репозитория для удаления данных из базы данных."""

    @abstractmethod
    async def exist(self, **kwargs: GetData) -> bool:
        """Абстрактный метод репозитория для поиска данных."""
