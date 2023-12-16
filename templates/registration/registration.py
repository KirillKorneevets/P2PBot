from fastapi import Request, APIRouter, Form
from fastapi.responses import HTMLResponse



from templates.base import templates


router = APIRouter()

@router.get("/registration", response_class=HTMLResponse)
def get_registration_form(request: Request):
    return templates.TemplateResponse("registration/registration_form.html", {"request": request})