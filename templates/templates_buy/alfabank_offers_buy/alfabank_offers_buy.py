from fastapi import FastAPI
from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from src.auth_depends.current_user import get_current_user
from src.requests.get_request_buy.alfabank_request_buy import get_alfabank_offers_buy
from templates.base import templates_buy


router = APIRouter()
app = FastAPI()


@router.get("/alfabank-offers-buy", response_class=HTMLResponse)
async def render_alfabank_offers_info(request: Request, offers_info: dict = Depends(get_alfabank_offers_buy), current_user: dict = Depends(get_current_user)):
    if isinstance(current_user, RedirectResponse):
        return current_user
    user = current_user.get("sub")
    if user:
        return templates_buy.TemplateResponse("alfabank_offers_buy/alfabank_offers_buy.html", {"request": request, "user_info": offers_info})
    else:
        raise HTTPException(status_code=405, detail="Method Not Allowed")

