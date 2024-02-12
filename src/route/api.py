from fastapi import APIRouter

from src.endpoint.bitpapa_tokens import router as bitpapa_token_post
from src.endpoint.auth import router as register_user_post
from src.endpoint.auth import router as login_user_post
from src.form_price_handlers.erip_sell import router as erip_form_sell_post
from src.form_price_handlers.erip_buy import router as erip_form_buy_post
from src.form_price_handlers.card2card_sell import router as card2card_form_sell_post
from src.form_price_handlers.card2card_buy import router as card2card_form_buy_post
from src.form_price_handlers.alfabank_sell import router as alfabank_form_sell_post
from src.form_price_handlers.alfabank_buy import router as alfabank_form_buy_post
from src.endpoint.activate_bot import router as activate_bot
from src.endpoint.bot_status import router as bot_status



from templates.registration.registration import router as registration_router_html
from templates.authorization.authorization_page import router as authorization_router_html
from templates.login.login import router as login_router_html
from templates.main_page.main_page import router as main_page_html
from templates.bitpapa_api_token.bitpapa_api_token import router as bitpapa_token_html
from templates.bitpapa_service.page_service_bitpapa import router as page_service_bitpapa_html
from templates.user_info.user_info import router as user_info_html
from templates.templates_sell.erip_request_templates.erip_offers_request import router as erip_offers_info_html
from templates.templates_sell.card2card_request_templates.card2card_offers_request import router as card2card_offers_info_html
from templates.templates_sell.alfabank_request_templates.alfabank_offers_request import router as alfabank_offers_info_html
from templates.templates_buy.erip_offers_buy.erip_offers_buy import router as erip_offers_buy_html
from templates.templates_buy.card2card_offers_buy.card2card_offers_buy import router as card2card_offers_buy_html
from templates.templates_buy.alfabank_offers_buy.alfabank_offers_buy import router as alfabank_offers_buy_html


router = APIRouter()


router.include_router(registration_router_html)
router.include_router(authorization_router_html)
router.include_router(login_router_html)
router.include_router(login_user_post)
router.include_router(register_user_post)


router.include_router(main_page_html)


router.include_router(bitpapa_token_post)
router.include_router(bitpapa_token_html)

router.include_router(page_service_bitpapa_html)


router.include_router(user_info_html)

router.include_router(erip_offers_info_html)
router.include_router(card2card_offers_info_html)
router.include_router(alfabank_offers_info_html)

router.include_router(erip_offers_buy_html)
router.include_router(card2card_offers_buy_html)
router.include_router(alfabank_offers_buy_html)


router.include_router(erip_form_sell_post)
router.include_router(erip_form_buy_post)
router.include_router(card2card_form_sell_post)
router.include_router(card2card_form_buy_post)
router.include_router(alfabank_form_sell_post)
router.include_router(alfabank_form_buy_post)


router.include_router(activate_bot)
router.include_router(bot_status)

