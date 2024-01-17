from src.models.models import User, PriceValue, BitpapaApiTokens
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi.responses import RedirectResponse
from fastapi import HTTPException, Depends


async def find_user_by_login_and_password(session: AsyncSession, username: str, password: str) -> object:
    try:
        result = await session.execute(
            select(User).filter(User.username == username, User.password == password)
        )
        return await result.scalar()
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        return None


async def add_user(session: AsyncSession, username: str, password: str):
    new_user = User(username=username, password=password)

    new_user.price_values.append(PriceValue())

    new_token = BitpapaApiTokens(api_token=None)
    new_user.api_tokens.append(new_token)

    session.add(new_user)
    await session.commit()

    return new_user


async def find_user_by_login(session: AsyncSession, username: str):
    try:
        result = await session.execute(select(User).filter(User.username == username).options(selectinload(User.price_values)))
        return result.scalars().first()
    except SQLAlchemyError as e:
        print(f"Произошла ошибка в find_user_by_login: {e}")
        return None


# def handle_current_user(current_user):
#     if isinstance(current_user, RedirectResponse):
#         return current_user
#     user = current_user.get("sub")
#     if user:
#         return user
#     else:
#         raise HTTPException(
#             status_code=401,
#             detail="Not authenticated",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

