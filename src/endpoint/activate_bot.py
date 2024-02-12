from fastapi import APIRouter, HTTPException, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.repo.services.activator import BotActivator
from src.auth_depends.current_user import get_current_user
from src.config.db_config import get_async_session
from src.repo import service


router = APIRouter()
activator = BotActivator()


@router.post("/activate-bot")
async def activate_bot(
    activate: bool = Form(...),
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
        user.is_bot_active = activate
        await session.commit()

        return {"message": "Bot activated" if activate else "Bot deactivated"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

