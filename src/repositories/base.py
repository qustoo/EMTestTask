from typing import List, Optional
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from interfaces.abstraction_repository import (AbstractRepository, EditData,
                                               GetData, RegisterData,
                                               TypeFilter, TypeID, TypeModel)


class BaseRepository(AbstractRepository):
    """Реализует базовые операции для моделей"""

    model: type[TypeModel]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, data: RegisterData) -> TypeID:
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get(self, **kwargs: GetData) -> Optional[TypeModel]:
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, filters: TypeFilter) -> Optional[List[TypeModel]]:
        raise NotImplementedError()

    async def edit(self, obj_id: TypeID, data: EditData) -> Optional[UUID]:
        stmt = (
            update(self.model)
            .filter(self.model.id == obj_id)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, obj_id: TypeID) -> Optional[TypeID]:
        stmt = delete(self.model).filter(self.model.id == obj_id).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def exist(self, obj_id: TypeID, **kwargs: GetData) -> bool:
        stmt = select(self.model).filter(self.model.id == obj_id).filter_by(**kwargs)
        obj = await self.session.execute(stmt)
        return bool(obj.scalar_one_or_none())
