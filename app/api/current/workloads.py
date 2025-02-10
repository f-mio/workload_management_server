# 標準モジュール
import datetime as dt
# サードパーティ製モジュール
from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi_csrf_protect import CsrfProtect
# プロジェクトモジュール
from services.auth import Auth_Utils
from services.workloads import (
    insert_workload_info_into_db, fetch_specify_workload,
    update_specify_workload,
    # fetch_specify_user_workloads_from_db,
    fetch_specify_condition_workloads_from_db,
)
from models.auth import CsrfType, ResponseMessage
from models.workloads import WorkloadInfoFromDB, WorkloadForm, WorkloadCondition, RegisteredWorkload


# 初期化処理
router = APIRouter(prefix="/api/workload")
auth = Auth_Utils()


@router.get("/db/{workload_id}", response_model=WorkloadInfoFromDB)
def api_fetch_workload_using_workload_id(workload_id: int):
    """
    idを指定した工数情報レコードの取得
    """
    workload = fetch_specify_workload(workload_id)
    return workload


@router.post("/db/post", response_model=ResponseMessage)
def api_insert_workload(input_form_value: WorkloadForm):
    """
    工数の登録
    """
    # [TODO] JWT検証処理を入れる
    # [TODO] CSRF検証処理を入れる
    # [TODO] rootユーザかどうかの判定

    # form値をdictに直し、更新日付を付与して登録用メソッドに渡す。
    workload_info = jsonable_encoder(input_form_value)
    workload_info["update_timestamp"] = dt.datetime.now()
    message = insert_workload_info_into_db(workload_info)

    return message


@router.put("/db/update/{workload_id}", response_model=ResponseMessage)
def api_update_workload(workload_id: int, form_value: WorkloadForm):
    """
    登録工数の編集
    """
    # [TODO] JWT検証処理を入れる
    # [TODO] CSRF検証処理を入れる
    # [TODO] rootユーザかどうかの判定

    # form値をdictに直し、データを更新用メソッドに渡す
    decoded_form_value = jsonable_encoder(form_value)
    message: dict = update_specify_workload(workload_id, decoded_form_value)
    return message


@router.post("/db/search", response_model=list[RegisteredWorkload])
def api_fetch_workloads_using_specify_condition(condition: WorkloadCondition):
    """
    指定条件の登録工数情報取得
    """
    condition = jsonable_encoder(condition)
    workloads = fetch_specify_condition_workloads_from_db(condition)
    return workloads
