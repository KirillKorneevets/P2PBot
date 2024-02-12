from fastapi import APIRouter, HTTPException, Depends, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse

from src.auth_depends.current_user import get_current_user
from src.config.db_config import get_async_session
from src.models.models import BitpapaApiTokens
from src.repo import service
from src.repo.exceptions import DuplicatedEntryError

router = APIRouter(
    prefix="/bitpapa",
    responses={404: {"description": "Not found"}}
)


@router.post("/get-token")
async def get_bitpapa_token(
        api_token: str = Form(...),
        session: AsyncSession = Depends(get_async_session),
        current_user: dict = Depends(get_current_user)
):
    redirect_url = "/bitpapa-user-info"

    if current_user is None or "id" not in current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if isinstance(current_user, RedirectResponse):
        return current_user

    user_id = current_user["id"]

    existing_token = await service.find_bitpapa_token(session, user_id)

    if existing_token:
        try:
            existing_token.api_token = api_token
            await session.commit()
            response = RedirectResponse(url=redirect_url)
            return response
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update API token: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="API token не найден")









