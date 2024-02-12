from fastapi import Request, APIRouter, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from templates.base import templates

from src.auth_depends.current_user import get_current_user



router = APIRouter()


@router.get("/get-token", response_class=HTMLResponse)
def get_api_token(request: Request, current_user: dict = Depends(get_current_user)):
    if isinstance(current_user, RedirectResponse):
        return current_user
    user = current_user.get("sub")
    if user:
        return templates.TemplateResponse("bitpapa_api_token/bitpapa_api_token.html", {"request": request})
    else:
        raise HTTPException(status_code=405, detail="Method Not Allowed")

