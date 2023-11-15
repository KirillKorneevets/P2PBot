from sqlalchemy import select, engine
from sqlalchemy.ext.asyncio import AsyncSession

from src.repo.models import User, PriceValue


async def find_user_by_login_and_password(session: AsyncSession, username: str, password: str) -> object:
    result: engine.Result = await session.execute(
        select(User).filter(User.username == username, User.password == password)
    )
    return result.scalar()


async def add_user(session: AsyncSession, username: str, password: str):
    new_user = User(username=username, password=password)
    new_price_value = PriceValue(max_price=None, min_price=None)
    new_user.price_values.append(new_price_value)

    session.add(new_user)
    await session.commit()

    return new_user


async def find_user_by_login(session: AsyncSession, username: str) -> object:
    result: engine.Result = await session.execute(
        select(User).filter(User.username == username)
    )
    return result.scalar()


