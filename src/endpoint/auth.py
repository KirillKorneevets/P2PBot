from fastapi import APIRouter, HTTPException, Depends, Request, Form, status
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.db_config import get_async_session
from src.repo import service
from src.repo.exceptions import DuplicatedEntryError
from src.repo.JWT import create_access_token, create_refresh_token


router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}}
)



@router.post("/registration")
def register_user(
    username: str = Form(...),
    password: str = Form(...),
    repeat_password: str = Form(...),
    session: AsyncSession = Depends(get_async_session)
):
    if password != repeat_password:
        return {"error": "Passwords do not match!"}

    existing_user = service.find_user_by_login(session, username)

    if existing_user:
        return {"Message": "User already exists"}

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)

    new_user = service.add_user(session, username, hashed_password)

    try:
        session.commit()
        return {"Message": "User registered successfully"}
    except IntegrityError as ex:
        session.rollback()
        raise DuplicatedEntryError("The User is already stored")



@router.post("/login")
async def login_user(
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_async_session),
):
    user_data = await service.find_user_by_login(session, username)
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    if pwd_context.verify(password, user_data.password):
        access_token = create_access_token({"sub": username})
        refresh_token = create_refresh_token({"sub": username})

        redirect_url = "/FlashCoinTrade"

        response = RedirectResponse(url=redirect_url)
        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True)
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )





