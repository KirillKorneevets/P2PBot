from src.auth_depends.current_user import get_current_user
from src.models.models import User, PriceValueBYN, BitpapaApiTokens, BitpapaUserName
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi.responses import RedirectResponse
from fastapi import HTTPException, Depends, status


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

    new_user.price_values.append(PriceValueBYN())

    new_token = BitpapaApiTokens(api_token=None)
    new_user.api_tokens.append(new_token)

    session.add(new_user)
    await session.commit()

    return new_user


async def find_user_by_login(session: AsyncSession, username: str):
    try:
        result = await session.execute(select(User).filter(User.username == username).options(selectinload(User.price_values)))
        user = result.scalars().first()

        return user

    except SQLAlchemyError as e:
        print(f"Произошла ошибка в find_user_by_login: {e}")
        return None

async def find_bitpapa_token(session: AsyncSession, user_id: str):
    try:
        result = await session.execute(
            select(BitpapaApiTokens).filter(BitpapaApiTokens.user_id == user_id)
        )
        bitpapa_token = result.scalars().first()

        return bitpapa_token

    except SQLAlchemyError as e:
        print(f"Произошла ошибка в find_bitpapa_token: {e}")
        return None

async def find_price_value(session: AsyncSession, user_id: str):
    try:
        result = await session.execute(
            select(PriceValueBYN).filter(PriceValueBYN.user_id == user_id)
        )
        return result.first()

    except SQLAlchemyError as e:
        print(f"Произошла ошибка в find_price_value: {e}")
        return None

async def find_user_by_id(session: AsyncSession, user_id: str):
    try:
        user = await session.get(User, user_id)
        return user

    except SQLAlchemyError as e:
        print(f"Произошла ошибка в find_user_by_id: {e}")
        return None


async def find_bitpapa_username(session: AsyncSession, user_id: str):
    try:
        stmt = select(BitpapaUserName.username).where(BitpapaUserName.user_id == user_id)
        result = await session.execute(stmt)
        username = result.scalar_one_or_none()
        return username

    except SQLAlchemyError as e:
        print(f"Произошла ошибка в find_bitpapa_username: {e}")
        return None

async def get_users_with_bot_active(session: AsyncSession):
    try:
        stmt = select(User).where(User.is_bot_active == True)
        result = await session.execute(stmt)
        return result.scalars().all()

    except SQLAlchemyError as e:
        print(f"Произошла ошибка в find_bitpapa_username: {e}")
        return None