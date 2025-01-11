# サードパーティ製モジュール
from fastapi import APIRouter, Depends, Response, Request
from fastapi_csrf_protect import CsrfProtect
# プロジェクトモジュール
from services.auth import Auth_Utils
from services.users import (fetch_user_using_specify_email, )
from models.auth import CsrfType
from models.users import UserInfo

router = APIRouter(
    prefix="/api/auth"
)
auth = Auth_Utils()

@router.get("/csrftoken", response_model=CsrfType)
async def get_csrf_token(response: Response, csrf_protect: CsrfProtect = Depends()):
    csrf_token, signed_token = csrf_protect.generate_csrf()
    response.set_cookie(
        key="fastapi_signed_token", value=signed_token,
        httponly=True, samesite="none", secure=True
    )
    res = { "csrf_token": csrf_token }
    return res


@router.get("/verify_jwt", response_model=UserInfo)
async def verify_jwt_token(request: Request):
    email = auth.verify_jwt(request)
    user_info = fetch_user_using_specify_email(email)
    return user_info
