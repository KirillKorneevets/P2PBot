from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

templates_buy = Jinja2Templates(directory="templates/templates_buy")

templates_sell = Jinja2Templates(directory="templates/templates_sell")

