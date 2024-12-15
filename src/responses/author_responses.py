from responses.base import BaseResponses
from schemas.authors_schemas import AuthorResponseSchema


class AuthorResponses(BaseResponses):

    POST_RESPONSES = {
        201: {"model": AuthorResponseSchema},
        **BaseResponses.CREATED_ITEM_RESPONSE,
        **BaseResponses.BAD_REQUEST,
        **BaseResponses.INTERNAL_ERROR_RESPONSE,
    }

    GET_RESPONSES = {
        200: {"model": AuthorResponseSchema},
        **BaseResponses.BAD_REQUEST,
        **BaseResponses.INTERNAL_ERROR_RESPONSE,
    }

    EDIT_RESPONSES = {
        200: {"model": AuthorResponseSchema},
        **BaseResponses.BAD_REQUEST,
        **BaseResponses.NOT_FOUND_RESPONSE,
        **BaseResponses.INTERNAL_ERROR_RESPONSE,
    }

    DELETE_RESPONSES = {
        200: {"model": AuthorResponseSchema},
        **BaseResponses.NOT_FOUND_RESPONSE,
        **BaseResponses.INTERNAL_ERROR_RESPONSE,
    }
