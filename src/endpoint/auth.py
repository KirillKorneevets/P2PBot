from fastapi import APIRouter, Cookie, HTTPException, Depends, Response, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from jose import JWTError, jwt

from src.endpoint.dto.UserLoginDto import UserLoginDto
from src.endpoint.dto.UserRegisterDto import UserRegisterDto
from src.config.db_config import get_session
from src.repo import service
from src.repo.exceptions import DuplicatedEntryError
from src.repo.JWT import create_access_token, SECRET_KEY, ALGORITHM







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

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(user.password)

    user = service.add_user(session, user.username, hashed_password)

    try:
        await session.commit()
        return user
    except IntegrityError as ex:
        await session.rollback()
        raise DuplicatedEntryError("The User is already stored")



@router.post("/login")
async def login_user(user: UserLoginDto, session: AsyncSession = Depends(get_session)):
    user_data = await service.find_user_by_login(session, user.username)
    if user_data is None:
        return {"Message": "Invalid username or password!"}

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    if pwd_context.verify(user.password, user_data.password):
        access_token = create_access_token({"sub": user.username})

        response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
        response.set_cookie("access_token", access_token)

        return response
    else:
        return {"Message": "Invalid username or password!"}

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/secure-data")
async def get_secure_data(current_user: dict = Depends(get_current_user)):
    return {"message": "SECRET DATA"}



