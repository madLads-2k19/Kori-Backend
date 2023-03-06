from fastapi import HTTPException, status


class KoriException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super(HTTPException, self).__init__(status_code, message)


class DuplicateRecordException(KoriException):
    def __init__(
        self,
        status_code: int = status.HTTP_409_CONFLICT,
        message: str = "Record already exists",
    ):
        super(KoriException, self).__init__(status_code, message)
