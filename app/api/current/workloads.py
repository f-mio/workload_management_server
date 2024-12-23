# 標準モジュール
import datetime as dt
# サードパーティ製モジュール
from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi_csrf_protect import CsrfProtect
# プロジェクトモジュール
from services.auth import Auth_Utils
from services.workload import (
    insert_workload_info_into_db,
)
from models.auth import CsrfType, ResponseMessage
from models.workloads import WorkloadInfoFromDB, WorkloadForm


# 初期化処理
router = APIRouter(prefix="/api/workload")
auth = Auth_Utils()


@router.get("/db", response_model=WorkloadInfoFromDB)
def api_fetch_workload_using_workload_id(workload_id: int):
    """
    idを指定した工数情報レコードの取得
    """
    pass


@router.post("/db/post")
def api_insert_workload_data(input_form_value: WorkloadForm):
    """
    工数の登録
    """
    # [TODO] JWT検証処理を入れる
    # [TODO] CSRF検証処理を入れる
    # [TODO] rootユーザかどうかの判定

    # データ加工
    workload_info = jsonable_encoder(input_form_value)
    workload_info["update_timestamp"] = dt.datetime.now()
    # SQLAlchemyを用いた登録処理
    message = insert_workload_info_into_db(workload_info)

    return message


@router.put("/db/edit")
def api_edit_registered_workload(workload_info: WorkloadForm):
    """
    登録工数の編集
    """
    pass


@router.get("/db/get", response_model=list[WorkloadInfoFromDB])
def api_fetch_workloads(user_id: int):
    """
    特定ユーザの登録工数情報取得
    """
    pass


@router.post("/db/search", response_model=list[WorkloadInfoFromDB])
def api_fetch_specify_condition_workloads(condition: dict):
    """
    指定条件の登録工数情報取得
    """
    pass
