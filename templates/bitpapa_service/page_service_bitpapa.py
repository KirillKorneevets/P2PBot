from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from templates.base import templates
from src.auth_depends.current_user import get_current_user

router = APIRouter()


@router.get("/bitpapa-service", response_class=HTMLResponse)
def get_page_service_bitpapa(request: Request, current_user: dict = Depends(get_current_user)):
    if isinstance(current_user, RedirectResponse):
        return current_user
    user = current_user.get("sub")
    if user:
        return templates.TemplateResponse("bitpapa_service/page_service_bitpapa.html", {"request": request, "user_id": user})
    else:
        raise HTTPException(status_code=405, detail="Method Not Allowed")

@router.post("/bitpapa-service", response_class=HTMLResponse)
def post_page_service_bitpapa(request: Request, current_user: dict = Depends(get_current_user)):
    if isinstance(current_user, RedirectResponse):
        return current_user
    user = current_user.get("sub")
    if user:
        return templates.TemplateResponse("bitpapa_service/page_service_bitpapa.html", {"request": request, "user_id": user})
    else:
        raise HTTPException(status_code=405, detail="Method Not Allowed")