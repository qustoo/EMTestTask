from typing import List
from uuid import UUID

from fastapi import APIRouter, Response, status

from api.dependices import BorrowFilterDep, BorrowServiceDep, LibraryUOWDep
from responses.borrow_response import BorrowResponses
from schemas.borrow_schemas import (BorrowedReturnSchema, BorrowRegisterSchema,
                                    BorrowResponseSchema, BorrowUpdateSchema)

borrow_router = APIRouter(prefix="/api/v1/borrows", tags=["Borrow"])


@borrow_router.post(
    path="/",
    summary="Создание записи о выдаче книги.",
    status_code=status.HTTP_201_CREATED,
    response_model=BorrowResponseSchema,
    responses=BorrowResponses.POST_RESPONSES,
)
async def create_borrows(
    uow: LibraryUOWDep,
    service: BorrowServiceDep,
    schema: BorrowRegisterSchema,
) -> Response:
    created_borrow = await service.add(uow, schema)
    return created_borrow


@borrow_router.get(
    path="/",
    summary="Получение списка всех выдач",
    status_code=status.HTTP_200_OK,
    response_model=List[BorrowResponseSchema],
    responses=BorrowResponses.GET_RESPONSES,
)
async def get_borrows(
    uow: LibraryUOWDep, service: BorrowServiceDep, filters: BorrowFilterDep
) -> Response:
    borrows = await service.get_all(uow, filters)
    return borrows


@borrow_router.get(
    path="/{borrow_id}/",
    summary="Получение информации о выдаче по id",
    status_code=status.HTTP_200_OK,
    response_model=BorrowResponseSchema,
    responses=BorrowResponses.GET_RESPONSES,
)
async def get_borrow(
    uow: LibraryUOWDep, service: BorrowServiceDep, borrow_id: UUID
) -> Response:
    borrow = await service.get(uow, borrow_id)
    return borrow


@borrow_router.patch(
    path="/{borrow_id}/",
    summary="Обновление информации и выдачи.",
    status_code=status.HTTP_200_OK,
    response_model=BorrowResponseSchema,
    responses=BorrowResponses.EDIT_RESPONSES,
)
async def update_borrow(
    uow: LibraryUOWDep,
    service: BorrowServiceDep,
    schema: BorrowUpdateSchema,
) -> Response:
    updated_borrow = await service.edit(uow, schema)
    return updated_borrow


@borrow_router.patch(
    path="/{borrow_id}/return/",
    summary="Завершение выдачи  с указанием даты возврата.",
    status_code=status.HTTP_200_OK,
    response_model=BorrowResponseSchema,
    responses=BorrowResponses.PATCH_RESPONSES,
)
async def return_borrow(
    uow: LibraryUOWDep,
    service: BorrowServiceDep,
    schema: BorrowedReturnSchema,
    borrow_id: UUID,
) -> Response:
    returned_borrow = await service.return_book(uow, borrow_id, schema)
    return returned_borrow
