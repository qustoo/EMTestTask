from schemas.borrow_schemas import BorrowedReturnSchema, BorrowResponseSchema

from .base import BaseResponses


class BorrowResponses(BaseResponses):
    POST_RESPONSES = {
        201: {"model": BorrowResponseSchema},
        **BaseResponses.CREATED_ITEM_RESPONSE,
        **BaseResponses.BAD_REQUEST,
        **BaseResponses.INTERNAL_ERROR_RESPONSE,
    }

    GET_RESPONSES = {
        200: {"model": BorrowResponseSchema},
        **BaseResponses.BAD_REQUEST,
        **BaseResponses.INTERNAL_ERROR_RESPONSE,
    }
    EDIT_RESPONSES = {
        200: {"model": BorrowResponseSchema},
    }
    PATCH_RESPONSES = {
        200: {"model": BorrowedReturnSchema},
    }
