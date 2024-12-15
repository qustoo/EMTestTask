from typing import List
from uuid import UUID

from fastapi import APIRouter, Response, status

from api.dependices import BookFilterDep, BookServiceDep, LibraryUOWDep
from responses.book_response import BookResponses
from schemas.book_schemas import (BookRegisterSchema, BookResponseSchema,
                                  BookUpdateSchema)

book_router = APIRouter(prefix="/api/v1/books", tags=["Books"])


@book_router.post(
    path="/",
    summary="Создание книги.",
    status_code=status.HTTP_201_CREATED,
    response_model=BookResponseSchema,
    responses=BookResponses.POST_RESPONSES,
)
async def create_book(
    uow: LibraryUOWDep,
    service: BookServiceDep,
    schema: BookRegisterSchema,
) -> Response:
    created_book = await service.add(uow, schema)
    return created_book


@book_router.get(
    path="/",
    summary="Получение списка книг",
    status_code=status.HTTP_200_OK,
    response_model=List[BookResponseSchema],
    responses=BookResponses.GET_RESPONSES,
)
async def get_books(
    uow: LibraryUOWDep, service: BookServiceDep, filters: BookFilterDep
) -> Response:
    books = await service.get_all(uow, filters)
    return books


@book_router.get(
    path="/{book_id}/",
    summary="Получение информации о книге.",
    status_code=status.HTTP_200_OK,
    response_model=BookResponseSchema,
    responses=BookResponses.GET_RESPONSES,
)
async def get_book(
    uow: LibraryUOWDep, service: BookServiceDep, book_id: UUID
) -> Response:
    book = await service.get(uow, book_id)
    return book


@book_router.put(
    path="/{book_id}/",
    summary="Обновление информации об книге.",
    status_code=status.HTTP_200_OK,
    response_model=BookResponseSchema,
    responses=BookResponses.EDIT_RESPONSES,
)
async def edit_book(
    uow: LibraryUOWDep,
    service: BookServiceDep,
    book_id: UUID,
    model: BookUpdateSchema,
) -> Response:
    updated_book = await service.edit(uow, book_id, model)
    return updated_book


@book_router.delete(
    path="/{book_id}/",
    summary="Удаление книги",
    status_code=status.HTTP_200_OK,
    response_model=BookResponseSchema,
    responses=BookResponses.DELETE_RESPONSES,
)
async def delete_author(
    uow: LibraryUOWDep,
    service: BookServiceDep,
    book_id: UUID,
) -> Response:
    deleted_book = await service.delete(uow, book_id)
    return deleted_book
