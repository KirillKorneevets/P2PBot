import httpx
import requests
from fastapi import Query
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth_depends.current_user import get_current_user
from src.config.db_config import get_async_session
from src.repo import service


async def post_erip__buy(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):

    if isinstance(current_user, RedirectResponse):
        return current_user

    if current_user is None or "id" not in current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = current_user["id"]

    bitpapa_api_token = await service.find_bitpapa_token(session, user_id)


    try:
        url = f"https://bitpapa.com/api/v1/pro/{id}"

        headers = {
            "Accept": "application/json",
            "X-Access-Token": bitpapa_api_token
        }

        params = {

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