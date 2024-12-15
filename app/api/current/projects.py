# 標準モジュール
import datetime as dt
# サードパーティ製モジュール
from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi_csrf_protect import CsrfProtect
# プロジェクトモジュール
from services.auth import Auth_Utils
from services.jira_contents import (
    fetch_all_projects_from_jira, upsert_project_info_into_db,
    fetch_all_projects_from_db,
)
from models.jira_contents import (
    ProjectInfoFromDB, ProjectInfoFromJira, ProjectForm,
    Response_Message,
)


# 初期化処理
router = APIRouter(prefix="/api/project")


@router.get("/jira/all", response_model=list[ProjectInfoFromJira])
async def fetch_all_jira_projects(response: Response, csrf_protect: CsrfProtect = Depends()):
    """
    JiraからAPIユーザの権限で取得できる全てのプロジェクトを取得してフロントに渡す。
    """
    # [TODO] JWT検証処理を入れる

    # サービス内のメソッドを用いてJiraからプロジェクトを取得する。
    projects = fetch_all_projects_from_jira()

    return projects


@router.get("/db/all")
async def fetch_all_db_project(response: Response, csrf_protect: CsrfProtect = Depends()):
    # [TODO] JWT検証処理を入れる
    projects = fetch_all_projects_from_db()
    return projects


@router.post("/db/update", response_model=Response_Message)
async def upsert_all_project_active_status(response: Response, form_value: ProjectForm, csrf_protect: CsrfProtect = Depends()):
    # [TODO] JWT検証処理を入れる
    # [TODO] CSRF検証処理を入れる
    # データ加工
    project_info = jsonable_encoder(form_value)
    project_info["is_target"] = True
    project_info["update_timestamp"] = dt.datetime.now()
    # SQLAlchemyを用いた登録処理
    message = upsert_project_info_into_db(project_info)

    return message


@router.post("/db/update/all")
async def all_update_projects_and_issues():
    pass
