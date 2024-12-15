from typing import List, Optional

from interfaces.abstraction_service import AbstractService, TypeID, TypeModel
from schemas.book_schemas import BookRegisterSchema, BookUpdateSchema
from schemas.filters import BookFilterSchema
from unit_of_works.librally_uow import LibraryUOW


class BookService(AbstractService):
    @classmethod
    async def add(cls, uow: LibraryUOW, schema: BookRegisterSchema) -> TypeID:
        data = schema.model_dump()
        async with uow:
            obj_id = await uow.books.add(data)
            await uow.commit()
            return obj_id

    @classmethod
    async def get(cls, uow: LibraryUOW, obj_id: TypeID) -> Optional[TypeModel]:
        async with uow:
            obj = await uow.books.get(obj_id=obj_id)
            return obj

    @classmethod
    async def get_all(
        cls,
        uow: LibraryUOW,
        filters: BookFilterSchema,
    ) -> Optional[List[TypeModel]]:
        async with uow:
            result = await uow.books.get_all(filters)
            return result

    @classmethod
    async def delete(cls, uow: LibraryUOW, obj_id: TypeID) -> Optional[TypeModel]:
        async with uow:
            result = await uow.books.delete(obj_id)
            await uow.commit()
            return result

    @classmethod
    async def exist(cls, uow: LibraryUOW, obj_id: TypeID) -> bool:
        async with uow:
            result = await uow.books.exist(obj_id)
            return result

    @classmethod
    async def edit(
        cls, uow: LibraryUOW, obj_id: TypeID, schema: BookUpdateSchema
    ) -> TypeModel:
        schema_exclude_unsets = schema.model_dump(exclude_unset=True)
        async with uow:
            result = await uow.books.edit(obj_id=obj_id, data=schema_exclude_unsets)
            await uow.commit()
            return result
