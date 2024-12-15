import uuid
from typing import List, Optional

from sqlalchemy import Select, func, select
from sqlalchemy.orm import selectinload

from interfaces.abstraction_repository import GetData, TypeID, TypeModel
from models.tables.author_table import Author
from repositories.base import BaseRepository
from schemas.filters import AuthorFilterSchema


class AuthorRepository(BaseRepository):
    model = Author

    def __get_base_limit_offset_stmt(self, filters: AuthorFilterSchema) -> Select:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.books))
            .limit(filters.limit)
            .offset(filters.offset)
        )
        return stmt

    def __is_authors_name(self, stmt: Select, filters: AuthorFilterSchema) -> Select:
        if filters.first_name:
            stmt = stmt.filter(self.model.first_name == filters.first_name)
        if filters.last_name:
            stmt = stmt.filter(self.model.last_name == filters.last_name)
        return stmt

    async def get_all(self, filters: AuthorFilterSchema) -> Optional[List[TypeModel]]:
        stmt = self.__get_base_limit_offset_stmt(filters)
        stmt = self.__is_authors_name(stmt, filters)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def book_count(self, author_id: uuid):
        stmt = func.count(self.model.books).where(self.model.id == author_id)
        result = await self.session.execute(stmt)
        count = result.scalar()
        return count

    async def get(self, obj_id: TypeID, **kwargs: GetData) -> Optional[TypeModel]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.books))
            .filter(self.model.id == obj_id)
            .filter_by(**kwargs)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
