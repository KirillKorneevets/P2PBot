from fastapi import Request, APIRouter, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from templates.base import templates
from src.auth_depends.current_user import get_current_user

router = APIRouter()


@router.get("/FlashCoinTrade", response_class=HTMLResponse)
def get_main_page(request: Request, current_user: dict = Depends(get_current_user)):
    if isinstance(current_user, RedirectResponse):
        return current_user
    user = current_user.get("sub")
    if user:
        return templates.TemplateResponse("main_page/main_page.html", {"request": request, "user_id": user})
    else:
        raise HTTPException(status_code=405, detail="Method Not Allowed")

@router.post("/FlashCoinTrade", response_class=HTMLResponse)
def post_main_page(request: Request, current_user: dict = Depends(get_current_user)):
    if isinstance(current_user, RedirectResponse):
        return current_user
    user = current_user.get("sub")
    if user:
        return templates.TemplateResponse("main_page/main_page.html", {"request": request, "user_id": user})
    else:
        raise HTTPException(status_code=405, detail="Method Not Allowed")

