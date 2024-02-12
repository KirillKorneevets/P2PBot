from fastapi import APIRouter, HTTPException, Depends, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import update

from src.auth_depends.current_user import get_current_user
from src.config.db_config import get_async_session
from src.models.models import PriceValueBYN
from src.repo import service
from templates.base import templates_buy
from src.requests.get_request_buy.alfabank_request_buy import get_alfabank_offers_buy


router = APIRouter()


@router.post("/alfabank-offers-buy")
async def add_alfabank_buy_price(
        request: Request,
        offers_info: dict = Depends(get_alfabank_offers_buy),
        price_value: float = Form(...),
        session: AsyncSession = Depends(get_async_session),
        current_user: dict = Depends(get_current_user)
):
    if isinstance(current_user, RedirectResponse):
        return current_user

    if current_user is None or "id" not in current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")


    user_id = current_user["id"]

    existing_value = await service.find_price_value(session, user_id)

    if existing_value:
        try:
            new_price_value = update(PriceValueBYN).where(PriceValueBYN.user_id == user_id).values(alfabank_buy=price_value)
            await session.execute(new_price_value)
            await session.commit()
            return templates_buy.TemplateResponse("alfabank_offers_buy/alfabank_offers_buy.html", {"request": request, "user_info": offers_info})
        except SQLAlchemyError as e:
            await session.rollback()
            error_message = f"Произошла ошибка при работе с базой данных: {e}"
            raise HTTPException(status_code=500, detail=error_message)
        except IntegrityError as e:
            await session.rollback()
            error_message = f"Произошла ошибка IntegrityError при сохранении цены в базе данных: {e}"
            raise HTTPException(status_code=422, detail=error_message)
        except Exception as e:
            await session.rollback()
            error_message = f"Произошла неизвестная ошибка: {e}"
            raise HTTPException(status_code=500, detail=error_message)