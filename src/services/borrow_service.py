from typing import List, Optional

from exceptions.exceptions_classes import (BadRequestException,
                                           BorrowedConflictException,
                                           NotFoundValueException)
from interfaces.abstraction_service import AbstractService, TypeID, TypeModel
from schemas.borrow_schemas import (BorrowedReturnSchema, BorrowRegisterSchema,
                                    BorrowUpdateSchema)
from schemas.filters import BorrowFilterSchema
from unit_of_works.librally_uow import LibraryUOW


class BorrowService(AbstractService):
    @classmethod
    async def add(cls, uow: LibraryUOW, schema: BorrowRegisterSchema) -> TypeID:
        return await cls.borrow(uow, schema)

    @classmethod
    async def get(cls, uow: LibraryUOW, obj_id: TypeID) -> Optional[TypeModel]:
        async with uow:
            obj = await uow.borrows.get(obj_id=obj_id)
            return obj

    @classmethod
    async def get_all(
        cls, uow: LibraryUOW, filters: BorrowFilterSchema
    ) -> Optional[List[TypeModel]]:
        async with uow:
            result = await uow.borrows.get_all(filters)
            return result

    @classmethod
    async def delete(cls, uow: LibraryUOW, obj_id: TypeID) -> TypeModel:
        async with uow:
            result = await uow.borrows.delete(obj_id)
            await uow.commit()
            return result

    @classmethod
    async def edit(
        cls, uow: LibraryUOW, obj_id: TypeID, schema: BorrowUpdateSchema
    ) -> TypeModel:
        schema_exclude_unsets = schema.model_dump(exclude_unset=True)
        async with uow:
            borrow_instance = await uow.borrows.edit(
                obj_id=obj_id, data=schema_exclude_unsets
            )
            await uow.commit()
            return borrow_instance

    @classmethod
    async def exist(cls, uow: LibraryUOW, obj_id: TypeID) -> bool:
        async with uow:
            result = await uow.borrows.exist(obj_id)
            return result

    @classmethod
    async def borrow(
        cls, uow: LibraryUOW, schema: BorrowRegisterSchema
    ) -> Optional[TypeModel]:
        book_id = schema.book_id
        data = schema.model_dump()
        async with uow:

            book_obj = await uow.books.get(book_id)

            if not book_obj:
                raise NotFoundValueException(
                    detail=f"Book with id = {book_id} not found"
                )
            if book_obj.count < 1:
                raise BadRequestException(
                    detail=f"There no available books left to borrow"
                )

            await uow.books.edit(obj_id=book_id, data={"count": book_obj.count - 1})
            borrow_obj = await uow.borrows.add(data)

            await uow.commit()
            return borrow_obj

    @classmethod
    async def return_book(
        cls, uow: LibraryUOW, obj_id: TypeID, schema: BorrowedReturnSchema
    ) -> TypeModel:
        book_id = schema.book_id
        async with uow:

            book_obj = await uow.books.get(book_id)
            borrow_obj = await uow.borrows.get(obj_id)

            if borrow_obj.return_date:
                raise BorrowedConflictException(
                    detail=f"Book with id = {book_id} already returned"
                )

            if not borrow_obj:
                raise NotFoundValueException(
                    detail=f"Borrow with id = {book_id} not found"
                )
            if not book_obj:
                raise NotFoundValueException(
                    detail=f"Book with id = {book_id} not found"
                )

            if borrow_obj.borrow_date < schema.return_date:
                raise BorrowedConflictException(
                    detail=f"return date cannot be early then borrow date"
                )

            await uow.books.edit(obj_id=book_id, data={"count": book_obj.count + 1})
            await uow.borrows.edit(
                obj_id=obj_id, data={"return_date": schema.return_date}
            )

            await uow.commit()
            return borrow_obj
