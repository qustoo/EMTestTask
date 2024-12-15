from schemas.book_schemas import BookResponseSchema

from .base import BaseResponses


class BookResponses(BaseResponses):

    POST_RESPONSES = {
        201: {"model": BookResponseSchema},
        **BaseResponses.CREATED_ITEM_RESPONSE,
        **BaseResponses.BAD_REQUEST,
        **BaseResponses.INTERNAL_ERROR_RESPONSE,
    }

    GET_RESPONSES = {
        200: {"model": BookResponseSchema},
        **BaseResponses.BAD_REQUEST,
        **BaseResponses.INTERNAL_ERROR_RESPONSE,
    }

    EDIT_RESPONSES = {
        200: {"model": BookResponseSchema},
        **BaseResponses.BAD_REQUEST,
        **BaseResponses.NOT_FOUND_RESPONSE,
        **BaseResponses.INTERNAL_ERROR_RESPONSE,
    }

    DELETE_RESPONSES = {
        200: {"model": BookResponseSchema},
        **BaseResponses.NOT_FOUND_RESPONSE,
        **BaseResponses.INTERNAL_ERROR_RESPONSE,
    }
