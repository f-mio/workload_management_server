# 標準モジュール
from typing import Any
# サードパーティ製モジュール
from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi_csrf_protect import CsrfProtect
# プロジェクトモジュール
from services.auth import Auth_Utils
from services.jira_contents import (fetch_all_projects_from_jira,)
from models.jira_contents import (
    ProjectInfoFromDB, ProjectInfoFromJira, ProjectForm
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
async def fetch_all_db_project():
    # [TODO] JWT検証処理を入れる
    pass

@router.post("/jira/update", response_model=ProjectInfoFromDB)
async def upsert_all_project_active_status(project_form: ProjectForm, response: Response, project_info: ProjectInfoFromDB, csrf_protect: CsrfProtect = Depends()):
    # [TODO] JWT検証処理を入れる
    # [TODO] CSRF検証処理を入れる
    pass
