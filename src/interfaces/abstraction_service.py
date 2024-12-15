from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar
from uuid import UUID

from models.base import Base
from schemas.filters import BaseFilterSchema
from unit_of_works.base import BaseUnitOfWork

TypeModel = TypeVar("TypeModel", bound=Base)
TypeDict = TypeVar("TypeDict", bound=dict)
TypeID = TypeVar("TypeID", int, UUID)
TypeUnitOfWork = TypeVar("TypeUnitOfWork", bound=BaseUnitOfWork)
TypeFilter = TypeVar("TypeFilter", bound=BaseFilterSchema)


class AbstractService(ABC):
    @classmethod
    @abstractmethod
    async def add(cls, uow: TypeUnitOfWork, obj_dict: TypeDict) -> Optional[TypeModel]:
        """Абстрактный метод сервиса для добавления данных."""

    @classmethod
    @abstractmethod
    async def get(cls, uow: TypeUnitOfWork, obj_id: TypeID) -> Optional[TypeModel]:
        """Абстрактный метод сервиса для получения данных."""

    @classmethod
    @abstractmethod
    async def get_all(
        cls, uow: TypeUnitOfWork, filters: Optional[TypeFilter]
    ) -> Optional[List[TypeModel]]:
        """Абстрактный метод сервиса для получения списка данных."""

    @classmethod
    @abstractmethod
    async def delete(cls, uow: TypeUnitOfWork, obj_id: TypeID) -> bool:
        """Абстрактный метод сервиса для удаления данных из базы данных."""

    @classmethod
    @abstractmethod
    async def edit(
        cls, uow: TypeUnitOfWork, obj_id: TypeID, obj_dict: TypeDict
    ) -> bool:
        """Абстрактный метод сервиса для редактирования данных."""

    @classmethod
    @abstractmethod
    async def exist(cls, uow: TypeUnitOfWork, obj_id: TypeID) -> bool:
        """Абстрактный метод для проверки наличия данных."""
