from lib2to3.fixes.fix_input import context
from typing import List, Optional

from exceptions.exceptions_classes import NotFoundValueException
from interfaces.abstraction_service import AbstractService, TypeID, TypeModel
from schemas.authors_schemas import AuthorRegisterSchema, AuthorUpdateSchema
from schemas.filters import AuthorFilterSchema
from unit_of_works.librally_uow import LibraryUOW


class AuthorService(AbstractService):
    @classmethod
    async def add(cls, uow: LibraryUOW, schema: AuthorRegisterSchema) -> TypeID:
        data = schema.model_dump()
        async with uow:
            obj_id = await uow.authors.add(data)
            await uow.commit()
            return obj_id

    @classmethod
    async def get(cls, uow: LibraryUOW, obj_id: TypeID) -> Optional[TypeModel]:
        async with uow:
            obj = await uow.authors.get(obj_id=obj_id)
            if not obj:
                raise NotFoundValueException(
                    detail=f"Author with id = {obj_id} not found"
                )
            return obj

    @classmethod
    async def get_all(
        cls, uow: LibraryUOW, filters: AuthorFilterSchema
    ) -> Optional[List[TypeModel]]:
        async with uow:
            result = await uow.authors.get_all(filters)
            return result

    @classmethod
    async def delete(cls, uow: LibraryUOW, obj_id: TypeID) -> Optional[TypeModel]:
        async with uow:
            result = await uow.authors.delete(obj_id)
            await uow.commit()
            return result

    @classmethod
    async def exist(cls, uow: LibraryUOW, obj_id: TypeID) -> bool:
        async with uow:
            result = await uow.authors.exist(obj_id)
            return result

    @classmethod
    async def edit(
        cls, uow: LibraryUOW, obj_id: TypeID, schema: AuthorUpdateSchema
    ) -> Optional[TypeModel]:
        schema_exclude_unsets = schema.model_dump(exclude_unset=True)
        async with uow:
            result = await uow.authors.edit(obj_id=obj_id, data=schema_exclude_unsets)
            await uow.commit()
            return result
