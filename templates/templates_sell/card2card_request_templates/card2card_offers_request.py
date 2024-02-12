from fastapi import FastAPI
from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from src.auth_depends.current_user import get_current_user
from src.requests.get_request_sell.card2card_request import get_card2card_offers
from templates.base import templates_sell


router = APIRouter()
app = FastAPI()


@router.get("/card2card-offers", response_class=HTMLResponse)
async def render_erip_offers_info(request: Request, offers_info: dict = Depends(get_card2card_offers), current_user: dict = Depends(get_current_user)):
    if isinstance(current_user, RedirectResponse):
        return current_user
    user = current_user.get("sub")
    if user:
        return templates_sell.TemplateResponse("card2card_request_templates/card2card_offers_request.html", {"request": request, "user_info": offers_info})
    else:
        raise HTTPException(status_code=405, detail="Method Not Allowed")

