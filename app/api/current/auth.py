# サードパーティ製モジュール
from fastapi import APIRouter, Depends
from fastapi_csrf_protect import CsrfProtect
# プロジェクトモジュール
from services.auth import Auth_Utils
from models.auth import CsrfType


router = APIRouter(
    prefix="/api"
)
auth = Auth_Utils()

@router.get("/csrftoken", response_model=CsrfType)
async def get_csrf_token(csrf_protect: CsrfProtect = Depends()):
    csrf_token, signed_token = csrf_protect.generate_csrf()
    res = {"csrf_token": csrf_token}
    return res
