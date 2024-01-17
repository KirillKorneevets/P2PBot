from fastapi import HTTPException


class DuplicatedEntryError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=422, detail=message)


class UserNotFoundException(Exception):
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)
