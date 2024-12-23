# サードパーティ製モジュール
from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi_csrf_protect import CsrfProtect
# プロジェクトモジュール
from services.auth import Auth_Utils
from services.users import (
    convert_password_to_hashed_one, verify_password_and_hashed_one,
    insert_new_user_into_app_db, verify_user_info_for_login )
from models.auth import CsrfType, ResponseMessage
from models.users import UserInfo, UserFormBody, LoginForm


# 初期化処理
router = APIRouter(prefix="/api/user")
auth = Auth_Utils()


@router.post("/signup", response_model=ResponseMessage)
async def api_user_signup(request: Request, user_form_value: UserFormBody, csrf_protect: CsrfProtect = Depends()):
    """
    サインアップ用エンドポイント
    """
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
async def api_user_signin(request: Request, login_form_value: LoginForm, response: Response):
    """
    サインイン用エンドポイント
    """
    form_value = jsonable_encoder(login_form_value)
    user_info = verify_user_info_for_login(form_value["email"], form_value["password"])

    return user_info



@router.get("/logout", response_model=ResponseMessage)
def api_logout_user_account():
    pass


@router.get("/deactivate", response_model=ResponseMessage)
def api_deactivate_user_account():
    pass


@router.get("/root/delete", response_model=ResponseMessage)
def api_delete_user_account_from_db(user_id: int):
    pass


@router.get("/root/activate", response_model=ResponseMessage)
def api_activate_user_account(user_id: int):
    pass


@router.get("/root/permission", response_model=ResponseMessage)
def api_grant_root_permission(user_id: int):
    pass
