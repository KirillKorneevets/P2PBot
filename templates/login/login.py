from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse



from templates.base import templates


router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})