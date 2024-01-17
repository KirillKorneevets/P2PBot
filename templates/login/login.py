from fastapi import Request, APIRouter, HTTPException
from fastapi.responses import HTMLResponse



from templates.base import templates


router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
@router.post("/login", response_class=HTMLResponse)
async def login(request: Request):
    if request.method == "GET":
        return templates.TemplateResponse("login/login.html", {"request": request})
    elif request.method == "POST":
        return templates.TemplateResponse("login/login.html", {"request": request})
    else:
        raise HTTPException(status_code=405, detail="Method Not Allowed")
