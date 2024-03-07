from fastapi import FastAPI
from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from src.auth_depends.current_user import get_current_user
from src.requests.user_info_request import get_bitpapa_user_info
from templates.base import templates


router = APIRouter()
app = FastAPI()


@router.get("/bitpapa-user-info", response_class=HTMLResponse)
@router.post("/bitpapa-user-info", response_class=HTMLResponse)
async def render_bitpapa_user_info(request: Request, user_info: dict = Depends(get_bitpapa_user_info), current_user: dict = Depends(get_current_user)):
    if isinstance(current_user, RedirectResponse):
        return current_user
    user = current_user.get("sub")
    if user:
        return templates.TemplateResponse("user_info/user_info_display.html", {"request": request, "user_info": user_info})
    else:
        raise HTTPException(status_code=405, detail="Method Not Allowed")

