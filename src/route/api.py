from fastapi import APIRouter
from src.endpoint import auth, offers

router = APIRouter()
offers_router = APIRouter()

router.include_router(auth.router)
offers_router.include_router(offers.router)
