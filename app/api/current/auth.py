# サードパーティ製モジュール
from fastapi import APIRouter, Depends, Response
from fastapi_csrf_protect import CsrfProtect
# プロジェクトモジュール
from services.auth import Auth_Utils
from models.auth import CsrfType


router = APIRouter(
    prefix="/api"
)
auth = Auth_Utils()

@router.get("/csrftoken", response_model=CsrfType)
async def get_csrf_token(response: Response, csrf_protect: CsrfProtect = Depends()):
    csrf_token, signed_token = csrf_protect.generate_csrf()
    response.set_cookie(
        key="fastapi_signed_token",
        value=signed_token,
        httponly=True,
        secure=True,
        samesite="none"
    )
    res = { "csrf_token": csrf_token }
    return res
