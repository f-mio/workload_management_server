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
    fetch_all_subtasks_with_path_from_db,
)
from models.auth import ResponseMessage
from models.jira_contents import (
    IssueInfoFromDB, SubtaskWithPath
)


# 初期化処理
router = APIRouter(prefix="/api/issue")


@router.get("/main-task/db/all", response_model=list[IssueInfoFromDB])
async def api_fetch_all_main_tasks():
    issues = fetch_all_main_issues_from_db()
    return issues


@router.get("/subtask/db/all", response_model=list[IssueInfoFromDB])
async def api_fetch_all_main_tasks():
    subtasks = fetch_all_subtasks_from_db()
    return subtasks


@router.get("/subtask_with_path/db/all", response_model=list[SubtaskWithPath])
async def api_fetch_all_main_tasks():
    subtasks = fetch_all_subtasks_with_path_from_db()
    return subtasks
