from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession


from src.auth_depends.current_user import get_current_user
from src.config.db_config import get_async_session
from src.repo import service

router = APIRouter()


@router.get("/get-bot-status")
async def get_bot_status(
    session: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(get_current_user)
):
    if isinstance(current_user, RedirectResponse):
        return current_user

    if current_user is None or "id" not in current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = current_user["id"]
    user = await service.find_user_by_id(session, user_id)

    if user:
        return JSONResponse(content={"status": "success", "is_bot_active": user.is_bot_active})
    else:
        raise HTTPException(status_code=404, detail="User not found")