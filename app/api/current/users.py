# サードパーティ製モジュール
from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi_csrf_protect import CsrfProtect
# プロジェクトモジュール
from services.auth import Auth_Utils
from services.users import (
    convert_password_to_hashed_one, verify_password_and_hashed_one,
    fetch_active_user_list,
    insert_new_user_into_app_db, verify_user_info_for_login )
from models.auth import CsrfType, ResponseMessage
from models.users import UserInfo, UserFormBody, LoginForm, UserListModel


# 初期化処理
router = APIRouter(prefix="/api/user")
auth = Auth_Utils()


@router.post("/signup", response_model=ResponseMessage)
async def api_user_signup(request: Request, user_form_value: UserFormBody, response: Response, csrf_protect: CsrfProtect = Depends()):
    """
    サインアップ用エンドポイント
    """
    # CSRF Token検証処理
    # csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
    # csrf_protect.validate_csrf(csrf_token)
    # フロントからの情報のデコード (Pydanticモデル → JSON)
    new_user = jsonable_encoder(user_form_value)
    # DB登録処理
    message, jwt_token = insert_new_user_into_app_db(new_user)
    response.set_cookie(
        key="access_token", value=f"Bearer {jwt_token}",
        httponly=True, samesite="none", secure=True
    )

    return message


@router.post("/signin", response_model=UserInfo)
async def api_user_signin(request: Request, login_form_value: LoginForm, response: Response):
    """
    サインイン用エンドポイント
    """
    form_value = jsonable_encoder(login_form_value)
    user_info, jwt_token = verify_user_info_for_login(form_value["email"], form_value["password"])
    response.set_cookie(
        key="access_token", value=f"Bearer {jwt_token}",
        httponly=True, samesite="none", secure=True
    )
    return user_info


@router.get("/active/all", response_model=list[UserListModel])
async def api_fetch_active_user_list(request: Request, response: Response):
    """
    有効なユーザ一覧を返却するエンドポイント
    """
    user_list = fetch_active_user_list()
    return user_list


@router.get("/logout", response_model=ResponseMessage)
def api_logout_user_account(response: Response):
    """
    ログアウト用エンドポイント
    """
    response.set_cookie(
        key="access_token", value="",
        httponly=True, samesite="none", secure=True
    )
    return


@router.get("/deactivate", response_model=ResponseMessage)
def api_deactivate_user_account(response: Response):
    """
    アカウント無効用のエンドポイント
    """
    # [TODO] 自身のアカウント無効化

    # JWT Tokenの無効化
    response.set_cookie(key="access_token", value="",
        httponly=True, samesite="none", secure=True
    )

    return


@router.get("/root/delete", response_model=ResponseMessage)
def api_delete_user_account_from_db(user_id: int):
    """
    管理者機能 アカウント削除用のエンドポイント
    """
    pass


@router.get("/root/activate", response_model=ResponseMessage)
def api_activate_user_account(user_id: int):
    """
    管理者機能 無効ユーザの有効化用エンドポイント
    """
    pass


@router.get("/root/permission", response_model=ResponseMessage)
def api_grant_root_permission(user_id: int):
    """
    管理者機能 管理者機能付与用エンドポイント
    """
    pass
