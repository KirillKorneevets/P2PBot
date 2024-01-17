# from fastapi import APIRouter, HTTPException, Depends, Request, Form
# from sqlalchemy.exc import IntegrityError
# from passlib.context import CryptContext
# from sqlalchemy.orm import Session
#
# from src.config.db_config import get_async_session
# from src.repo import service
# from src.repo.exceptions import DuplicatedEntryError
#
#
# router = APIRouter(
#     prefix="/auth",
#     responses={404: {"description": "Not found"}}
# )
#
#
# @router.post("/registration")
# def register_user(
#     token: str = Form(...),
#     session: Session = Depends(get_async_session)
# ):
#
#
#
#     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#     hashed_password = pwd_context.hash(password)
#
#     new_user = service.add_user(session, username, hashed_password)
#
#     try:
#         session.commit()
#         return {"Message": "User registered successfully"}
#     except IntegrityError as ex:
#         session.rollback()
#         raise DuplicatedEntryError("The User is already stored")