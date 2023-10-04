from fastapi import Cookie, HTTPException, Response, APIRouter
from jose import JWTError, jwt
from datetime import datetime, timedelta


SECRET_KEY = "ia@sdi#213*kaas#%lasd@nmo202103&jkmas@lasmld%$olado12312348kas@dk3oanao#@"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}}
)

def create_access_token(data: dict, expires_delta: timedelta = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        expire = datetime.utcnow() + expires_delta

        data_with_expiry = dict(data, exp=expire)
        return jwt.encode(data_with_expiry, SECRET_KEY, algorithm=ALGORITHM)

