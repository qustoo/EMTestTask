from typing import List, Optional

from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload, selectinload

from models.tables.author_table import Book
from repositories.base import BaseRepository, GetData, TypeID, TypeModel
from schemas.filters import BookFilterSchema


class BookRepository(BaseRepository):
    model = Book

    def __get_base_limit_offset_stmt(self, filters: BookFilterSchema) -> Select:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.borrows))
            .options(joinedload(self.model.author))
            .limit(filters.limit)
            .offset(filters.offset)
        )
        return stmt

    def __is_gt_count(self, stmt: Select, filters: BookFilterSchema) -> Select:
        if filters.count:
            stmt = stmt.filter(self.model.count > filters.count)
        return stmt

    async def get_all(self, filters: BookFilterSchema) -> Optional[List[TypeModel]]:
        stmt = self.__get_base_limit_offset_stmt(filters)
        stmt = self.__is_gt_count(stmt, filters)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get(self, obj_id: TypeID, **kwargs: GetData) -> Optional[TypeModel]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.borrows))
            .options(joinedload(self.model.author))
            .filter(self.model.id == obj_id)
            .filter_by(**kwargs)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
