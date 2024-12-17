# サードパーティ製モジュール
from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi_csrf_protect import CsrfProtect
# プロジェクトモジュール
from services.auth import Auth_Utils
from services.users import (
    convert_password_to_hashed_one, verify_password_and_hashed_one,
    insert_new_user_into_app_db, verify_user_info_for_login )
from models.auth import CsrfType, SuccessMessage
from models.users import UserInfo, UserFormBody, LoginForm


# 初期化処理
router = APIRouter(prefix="/api/user")
auth = Auth_Utils()


# サインアップ用エンドポイント
@router.post("/signup", response_model=SuccessMessage)
async def user_signup(request: Request, user_form_value: UserFormBody, csrf_protect: CsrfProtect = Depends()):
    # CSRF Token検証処理
    # csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
    # csrf_protect.validate_csrf(csrf_token)
    # フロントからの情報のデコード (Pydanticモデル → JSON)
    new_user = jsonable_encoder(user_form_value)
    # DB登録処理
    message = insert_new_user_into_app_db(new_user)
    return message


# サインイン用エンドポイント
@router.post("/signin", response_model=UserInfo)
async def user_signin(request: Request, login_form_value: LoginForm, response: Response):

    form_value = jsonable_encoder(login_form_value)
    user_info = verify_user_info_for_login(form_value["email"], form_value["password"])

    return user_info
