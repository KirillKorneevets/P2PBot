import httpx
import asyncio
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import FastAPI

from src.auth_depends.current_user import get_current_user
from src.config.db_config import get_async_session
from src.models.models import PriceValueBYN, User
from src.repo import service
from src.repo.service import get_users_with_bot_active
from src.requests.get_request_buy.erip_request_buy import get_erip_offers_buy

app = FastAPI()

async def post_erip_buy(
    session: AsyncSession = Depends(get_async_session),
):
    users = await get_users_with_bot_active(session)
    for user in users:
        user_id = user.id
        bitpapa_api_token = await service.find_bitpapa_token(session, user_id)
        api_token = bitpapa_api_token.api_token
        bitpapa_username = await service.find_bitpapa_username(session, user_id)
        stmt = select(PriceValueBYN.erip_buy).where(PriceValueBYN.user_id == user_id)
        result = await session.execute(stmt)
        erip_buy_value = result.scalar_one_or_none()

        try:
            erip_offers = await get_erip_offers_buy(crypto_currency_code="BTC",
                                                    currency_code="BYN",
                                                    payment_method_bank_code="B34",
                                                    payment_method_code="SPECIFIC_BANK",
                                                    sort="-price",
                                                    offer_type="buy")

            prices = sorted([offer['price'] for offer in erip_offers['ads']], reverse=True)

            updated_price = None
            for price in prices:
                if erip_buy_value < price:
                    continue
                else:
                    updated_price = price
                    break

            if updated_price is None:
                print(f"Для пользователя {bitpapa_username} не найдено подходящих предложений для обновления цены.")
                continue


            matching_offer_id = None
            for offer in erip_offers['ads']:
                if offer['user_name'] == bitpapa_username:
                    matching_offer_id = offer['id']


            url = f"https://bitpapa.com/api/v1/pro/{matching_offer_id}"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-Access-Token": api_token
            }
            new_equation = {"equation": str(updated_price + 0.01)}
            async with httpx.AsyncClient() as client:
                response = await client.put(url, headers=headers, json=new_equation)
                if response.status_code == 200:
                    print(f"Цена для {bitpapa_username} успешно обновлена.")
                else:
                    print(f"Ошибка обновления цены: {response.text}")


        except httpx.HTTPStatusError as e:
            return JSONResponse(content={"error": f"Ошибка при запросе данных: {str(e)}"}, status_code=500)

        except httpx.RequestError as e:
            return JSONResponse(content={"error": f"Ошибка при формировании запроса: {str(e)}"}, status_code=500)

        except httpx.TimeoutException as e:
            return JSONResponse(content={"error": f"Превышен таймаут запроса: {str(e)}"}, status_code=500)





async def post_erip_buy_task():
    while True:
        try:
            async for session in get_async_session():
                await post_erip_buy(session=session)
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Ошибка в задаче post_erip_buy_task: {e}")
            await asyncio.sleep(1)