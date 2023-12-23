from fastapi import APIRouter, HTTPException, Depends, Request, Form
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.config.db_config import get_sync_session
from src.repo import service
from src.repo.exceptions import DuplicatedEntryError
from src.repo.JWT import create_access_token, SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}}
)



@router.post("/registration")
def register_user(
    username: str = Form(...),
    password: str = Form(...),
    repeat_password: str = Form(...),
    session: Session = Depends(get_sync_session)
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
def login_user(
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_sync_session)
):
    user_data = service.find_user_by_login(session, username)
    if user_data is None:
        return {"Message": "Invalid username or password!"}

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    if pwd_context.verify(password, user_data.password):
        access_token = create_access_token({"sub": username})

        response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
        response.set_cookie(key="access_token", value=access_token, httponly=True)

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
def get_secure_data(current_user: dict = Depends(get_current_user)):
    return {"message": "SECRET DATA"}



