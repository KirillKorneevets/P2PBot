from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

from templates.base import templates


router = APIRouter()


@router.get("/authorization", response_class=HTMLResponse)
def get_authorization(request: Request):
    return templates.TemplateResponse("authorization/authorization.html", {"request": request})