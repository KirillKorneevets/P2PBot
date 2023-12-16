from fastapi import APIRouter
from src.endpoint.auth import router as register_user_post
from src.endpoint.auth import router as login_user_post
from templates.registration.registration import router as registration_router_html
from templates.authorization.authorization_page import router as authorization_router_html
from templates.login.login import router as login_router_html


router = APIRouter()


router.include_router(registration_router_html)
router.include_router(authorization_router_html)
router.include_router(login_router_html)
router.include_router(login_user_post)
router.include_router(register_user_post)

