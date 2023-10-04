from pydantic import BaseModel


class UserRegisterDto(BaseModel):
    username: str
    password: str
    repeatPassword: str
