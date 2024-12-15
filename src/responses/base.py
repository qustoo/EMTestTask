from responses import responses_classes as responses


class BaseResponses:
    SUCCESS_RESPONSE = {200: {"model": responses.SuccessIdResponseSchema}}
    CREATED_ITEM_RESPONSE = {201: {"model": responses.SuccessCreatedItemResponse}}
    BAD_REQUEST = {400: {"model": responses.BadRequestResponseSchema}}
    NOT_FOUND_RESPONSE = {404: {"model": responses.NotFoundResponseSchema}}
    INTERNAL_ERROR_RESPONSE = {500: {"model": responses.ServerErrorResponseSchema}}
