from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth_depends.current_user import get_current_user
from src.repo import service
from src.models.models import User, PriceValueBYN


class BotActivator:
    async def activate_field(self, user, session, field_name):
        setattr(user, f'is_{field_name}_active', True)
        await session.commit()

    async def deactivate_field(self, user, session, field_name):
        setattr(user, f'is_{field_name}_active', False)
        await session.commit()