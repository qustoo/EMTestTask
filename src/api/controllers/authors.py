from typing import List
from uuid import UUID

from fastapi import APIRouter, Response
from starlette import status

from api.dependices import AuthorFilterDep, AuthorServiceDep, LibraryUOWDep
from responses.author_responses import AuthorResponses
from schemas.authors_schemas import (AuthorRegisterSchema,
                                     AuthorResponseSchema, AuthorUpdateSchema)

author_router = APIRouter(prefix="/api/v1/authors", tags=["Authors"])


@author_router.post(
    path="/",
    summary="Создание автора",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthorResponseSchema,
    responses=AuthorResponses.POST_RESPONSES,
)
async def create_author(
    uow: LibraryUOWDep,
    service: AuthorServiceDep,
    schema: AuthorRegisterSchema,
) -> Response:
    created_author = await service.add(uow, schema)
    return created_author


@author_router.get(
    path="/",
    summary="Получение списка авторов",
    status_code=status.HTTP_200_OK,
    response_model=List[AuthorResponseSchema],
    responses=AuthorResponses.GET_RESPONSES,
)
async def get_authors(
    uow: LibraryUOWDep,
    service: AuthorServiceDep,
    filters: AuthorFilterDep,
) -> Response:
    authors = await service.get_all(uow, filters)
    return authors


@author_router.get(
    path="/{author_id}/",
    summary="Получение информации об авторе по id",
    status_code=status.HTTP_200_OK,
    response_model=AuthorResponseSchema,
    responses=AuthorResponses.GET_RESPONSES,
)
async def get_author(
    uow: LibraryUOWDep,
    service: AuthorServiceDep,
    author_id: UUID,
) -> Response:
    author = await service.get(uow, author_id)
    return author


@author_router.put(
    path="/{author_id}/",
    summary="Обновление информации об авторе ",
    status_code=status.HTTP_200_OK,
    response_model=AuthorResponseSchema,
    responses=AuthorResponses.EDIT_RESPONSES,
)
async def edit_author(
    uow: LibraryUOWDep,
    service: AuthorServiceDep,
    author_id: UUID,
    model: AuthorUpdateSchema,
) -> Response:
    updated_author = await service.edit(uow, author_id, model)
    return updated_author


@author_router.delete(
    path="/{author_id}/",
    summary="Удаление автора",
    status_code=status.HTTP_200_OK,
    response_model=AuthorResponseSchema,
    responses=AuthorResponses.DELETE_RESPONSES,
)
async def delete_author(
    uow: LibraryUOWDep,
    service: AuthorServiceDep,
    author_id: UUID,
) -> Response:
    deleted_author = await service.delete(uow, author_id)
    return deleted_author
