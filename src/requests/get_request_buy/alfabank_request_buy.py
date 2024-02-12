import httpx
import requests
from fastapi import Query
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth_depends.current_user import get_current_user
from src.config.db_config import get_async_session


async def get_alfabank_offers_buy(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
    crypto_currency_code: str = Query("BTC", description="Код криптовалюты"),
    currency_code: str = Query("BYN", description="Код фиатной валюты"),
    payment_method_bank_code: str = Query("B2", description="Код банка из справочников банков"),
    payment_method_code: str = Query("SPECIFIC_BANK", description="Код методов оплаты из справочников методов оплаты"),
    sort: str = Query("-price", description="Поля для сортировки"),
    offer_type: str = Query("buy", description="Покупка или продажа")
):

    if isinstance(current_user, RedirectResponse):
        return current_user

    try:
        url = "https://bitpapa.com/api/v1/partners/ads/search"

        headers = {
            "Accept": "application/json",
            "X-Access-Token": "123"
        }

        params = {
            "crypto_currency_code": crypto_currency_code,
            "currency_code": currency_code,
            "payment_method_bank_code": payment_method_bank_code,
            "payment_method_code": payment_method_code,
            "sort": sort,
            "type": offer_type
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            json_data = response.json()
            return json_data
    except requests.RequestException as e:
        return JSONResponse(content={"error": f"Ошибка при запросе данных: {str(e)}"}, status_code=500)

    except (requests.RequestException, httpx.RequestError) as e:
        return JSONResponse(content={"error": f"Ошибка при формировании запроса: {str(e)}"}, status_code=500)

    except httpx.TimeoutException as e:
        return JSONResponse(content={"error": f"Превышен таймаут запроса: {str(e)}"}, status_code=500)