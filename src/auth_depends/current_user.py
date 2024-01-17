import os
from typing import Union
from jose import jwt
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends, status, Request
from fastapi.responses import RedirectResponse as AsyncRedirectResponse

from src.config.db_config import get_async_session
from src.repo import service
from src.repo.JWT import create_access_token
from src.repo.exceptions import UserNotFoundException


load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')


async def get_current_user(session: AsyncSession = Depends(get_async_session), request: Request = None) -> Union[None, AsyncRedirectResponse]:
    """"
    This function provides the authentication logic.
    It checks the JWT in the cookies and updates the access token if necessary.
    Or it returns to the login page
    """

    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if not access_token or not refresh_token:
        return await redirect_to_login()


    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await service.find_user_by_login(session, username)
        if user is None:
            raise UserNotFoundException("User not found")

    except jwt.ExpiredSignatureError:
        if refresh_token:
            try:
                decoded_refresh_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
                new_access_token = create_access_token({"sub": decoded_refresh_token["sub"]})
                response = AsyncRedirectResponse(url=request.url.path)
                response.set_cookie("access_token", new_access_token, httponly=True)
                return response
            except jwt.JWTError:
                return await redirect_to_login()
        else:
            return await redirect_to_login()

    except jwt.JWTError:
        if refresh_token:
            try:
                decoded_refresh_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
                new_access_token = create_access_token({"sub": decoded_refresh_token["sub"]})
                response = AsyncRedirectResponse(url=request.url.path)
                response.set_cookie("access_token", new_access_token, httponly=True)
                return response
            except jwt.JWTError:
                return await redirect_to_login()
        else:
            return await redirect_to_login()

    return {"sub": username, "scopes": payload.get("scopes", [])}


async def redirect_to_login():
    response = AsyncRedirectResponse(url="/login")
    return response
