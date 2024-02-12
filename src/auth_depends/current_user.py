import os
from typing import Union
from jose import jwt
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends, status, Request
from fastapi.responses import RedirectResponse

from src.config.db_config import get_async_session
from src.repo.JWT import create_access_token


load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')


async def get_current_user(request: Request = None) -> Union[None, RedirectResponse, dict]:
    """
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
        user_id: str = payload.get("id")

    except jwt.ExpiredSignatureError:
        if refresh_token:
            try:
                decoded_refresh_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
                new_access_token = create_access_token({"sub": decoded_refresh_token["sub"], "id": decoded_refresh_token.get("id")})
                response = RedirectResponse(url=request.url.path)
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
                new_access_token = create_access_token({"sub": decoded_refresh_token["sub"], "id": decoded_refresh_token.get("id")})
                response = RedirectResponse(url=request.url.path)
                response.set_cookie("access_token", new_access_token, httponly=True)
                return response
            except jwt.JWTError:
                return await redirect_to_login()
        else:
            return await redirect_to_login()


    return {"sub": username, "id": user_id, "scopes": payload.get("scopes", [])}


async def redirect_to_login():
    response = RedirectResponse(url="/authorization")
    return response


