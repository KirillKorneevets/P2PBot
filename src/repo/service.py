from sqlalchemy import select, engine
from sqlalchemy.ext.asyncio import AsyncSession

from src.repo.models import User


async def find_user_by_login_and_password(session: AsyncSession, username: str, password: str) -> object:
    result: engine.Result = await session.execute(
        select(User).filter(User.username == username, User.password == password))
    return result.scalar()


def add_user(session: AsyncSession, username: str, password: str):
    new_user = User(username=username, password=password)
    session.add(new_user)
    return new_user


async def find_user_by_login(session: AsyncSession, username: str) -> object:
    result: engine.Result = await session.execute(
        select(User).filter(User.username == username))
    return result.scalar()
