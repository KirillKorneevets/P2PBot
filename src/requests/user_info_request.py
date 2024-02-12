import httpx
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse, RedirectResponse

from src.auth_depends.current_user import get_current_user
from src.config.db_config import get_async_session
from src.models.models import BitpapaApiTokens
from src.repo.service import find_bitpapa_token

router = APIRouter()


async def get_bitpapa_user_info(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if isinstance(current_user, RedirectResponse):
        return current_user

    try:
        bitpapa_token = await find_bitpapa_token(session, current_user["id"])

        if bitpapa_token:
            url = "https://bitpapa.com/api/v1/me"
            api_token = bitpapa_token.api_token

            headers = {
                "Accept": "application/json",
                "X-Access-Token": api_token
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                json_data = response.json()

                user_info = json_data.get("user", {})
                result = {"balance": user_info.get("balance"), "user_name": user_info.get("user_name")}
                username = result.get("user_name")
                return result
        else:
            raise HTTPException(status_code=401, detail="Bitpapa API token not found for the user")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error making request to Bitpapa API: {str(e)}")

