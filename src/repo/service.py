from sqlalchemy import select, engine
from sqlalchemy.orm import Session
from src.models.models import User, PriceValue, BitpapaApiTokens


def find_user_by_login_and_password(session: Session, username: str, password: str) -> object:
    result: engine.Result = session.execute(
        select(User).filter(User.username == username, User.password == password)
    )
    return result.scalar()


def add_user(session: Session, username: str, password: str):
    new_user = User(username=username, password=password)

    new_user.price_values.append(PriceValue())

    new_token = BitpapaApiTokens(api_token=None)
    new_user.api_tokens.append(new_token)

    session.add(new_user)
    session.commit()

    return new_user


def find_user_by_login(session: Session, username: str) -> object:
    result: engine.Result = session.execute(
        select(User).filter(User.username == username)
    )
    return result.scalar()


