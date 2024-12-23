# 標準モジュール
import datetime as dt
# サードパーティ製モジュール
from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi_csrf_protect import CsrfProtect
# プロジェクトモジュール
from services.auth import Auth_Utils
from services.jira_contents import (
    fetch_all_main_issues_from_db, fetch_all_subtasks_from_db,
)
from models.auth import ResponseMessage
from models.jira_contents import (
    IssueInfoFromDB
)


# 初期化処理
router = APIRouter(prefix="/api/issue")


@router.get("/api/issue/main-task/db/all", response_model=list[IssueInfoFromDB])
async def api_fetch_all_main_tasks():
    issues = fetch_all_main_issues_from_db()
    return issues


@router.get("/api/issue/subtask/db/all", response_model=list[IssueInfoFromDB])
async def api_fetch_all_main_tasks():
    subtasks = fetch_all_subtasks_from_db()
    return subtasks
