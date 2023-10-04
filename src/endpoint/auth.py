from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.endpoint.dto.UserLoginDto import UserLoginDto
from src.endpoint.dto.UserRegisterDto import UserRegisterDto
from src.config.db_config import get_session
from src.repo import service
from src.repo.exceptions import DuplicatedEntryError
from src.repo.JWT import create_access_token, SECRET_KEY, ALGORITHM

from fastapi import Cookie, HTTPException, Depends, Response
from jose import JWTError, jwt





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

    access_token = create_access_token({"sub": user.username})

    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie("access_token", access_token)

    return response

@router.get("/secure-data")
async def get_secure_data(response: Response, token: str = Cookie(None)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Could not identify user")
        return {"message": "Access granted for user: " + username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
