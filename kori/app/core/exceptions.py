from fastapi import HTTPException, status


class KoriException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super(HTTPException, self).__init__(status_code, message)


class BadRequestException(KoriException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        message: str = "Bad Request",
    ):
        super(KoriException, self).__init__(status_code, message)


class ForbiddenException(KoriException):
    def __init__(
        self,
        status_code: int = status.HTTP_403_FORBIDDEN,
        message: str = "Access forbidden",
    ):
        super(KoriException, self).__init__(status_code, message)


class NotFoundException(KoriException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        message: str = "Record not found",
    ):
        super(KoriException, self).__init__(status_code, message)


class DuplicateRecordException(KoriException):
    def __init__(
        self,
        status_code: int = status.HTTP_409_CONFLICT,
        message: str = "Record already exists",
    ):
        super(KoriException, self).__init__(status_code, message)
