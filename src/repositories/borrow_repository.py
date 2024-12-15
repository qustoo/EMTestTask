from typing import List, Optional

from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload

from models.tables.borrow_table import Borrow
from repositories.base import BaseRepository, GetData, TypeID, TypeModel
from schemas.filters import BorrowFilterSchema


class BorrowRepository(BaseRepository):
    model = Borrow

    def __get_base_limit_offset_stmt(self, filters: BorrowFilterSchema) -> Select:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.book))
            .limit(filters.limit)
            .offset(filters.offset)
        )
        return stmt

    def __is_later_returned_date(
        self, stmt: Select, filters: BorrowFilterSchema
    ) -> Select:
        if filters.return_date:
            stmt = stmt.filter(self.model.return_date > filters.return_date)
        return stmt

    async def get_all(self, filters: BorrowFilterSchema) -> Optional[List[TypeModel]]:
        stmt = self.__get_base_limit_offset_stmt(filters)
        stmt = self.__is_later_returned_date(stmt, filters)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get(self, obj_id: TypeID, **kwargs: GetData) -> Optional[TypeModel]:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.book))
            .filter(self.model.id == obj_id)
            .filter_by(**kwargs)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
