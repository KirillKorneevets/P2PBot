from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import httpx

router = APIRouter(
    prefix="/offers",
    responses={404: {"description": "Not found"}}
)



@router.get("/info")
async def get_offers(
    crypto_currency_code: str = Query("BTC", description="Код криптовалюты"),
    currency_code: str = Query("BYN", description="Код фиатной валюты"),
    payment_method_bank_code: str = Query("B34", description="Код банка из справочников банков"),
    payment_method_code: str = Query("SPECIFIC_BANK", description="Код методов оплаты из справочников методов оплаты"),
    sort: str = Query("price", description="Поля для сортировки"),
    offer_type: str = Query("sell", description="Покупка или продажа")
):
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
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return JSONResponse(content=data)
        except httpx.RequestError as e:
            return JSONResponse(content={"error": f"Ошибка при запросе данных: {str(e)}"}, status_code=500)
