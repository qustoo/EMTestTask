from fastapi import HTTPException, status

from consts.values import BAD_REQUEST, BORROW_CONFLICT, ITEM_NOT_FOUND


class NotFoundValueException(HTTPException):
    def __init__(self, detail: str = ITEM_NOT_FOUND) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class BorrowedConflictException(HTTPException):
    def __init__(self, detail: str = BORROW_CONFLICT) -> None:
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class BadRequestException(HTTPException):
    def __init__(self, detail: str = BAD_REQUEST) -> None:
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail
