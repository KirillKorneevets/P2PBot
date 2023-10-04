from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.endpoint.dto.UserLoginDto import UserLoginDto
from src.endpoint.dto.UserRegisterDto import UserRegisterDto
from src.config.db_config import get_session
from src.repo import service
from src.repo.exceptions import DuplicatedEntryError

router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}}
)



@router.post("/registration")
async def register_user(user: UserRegisterDto, session: AsyncSession = Depends(get_session)):
    if user.password != user.repeatPassword:
        return {"error": "Passwords does not match!"}

    existing_user = await service.find_user_by_login(session, user.username)

    if existing_user:
        return {"Message": "User already exists"}

    user = service.add_user(session, user.username, user.password)

    try:
        await session.commit()
        return user
    except IntegrityError as ex:
        await session.rollback()
        raise DuplicatedEntryError("The User is already stored")



@router.post("/login")
async def login_user(user: UserLoginDto, session: AsyncSession = Depends(get_session)):
    user = await service.find_user_by_login_and_password(session, user.username, user.password)
    if user is None:
        return {"Message": "Invalid username or password!"}
    return user
