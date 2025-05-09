# 標準モジュール
import datetime as dt
# サードパーティ製モジュール
from pydantic import BaseModel


class ProjectInfoFromDB(BaseModel):
    id: int
    name: str
    jira_key: str
    description: str
    is_target: bool # root userのみ変更可能
    update_timestamp: dt.datetime
    create_timestamp: dt.datetime


class ProjectInfoFromJira(BaseModel):
    id: int
    name: str
    jira_key: str
    description: str
    is_target: bool # root userのみ変更可能


class ProjectForm(BaseModel):
    id: int
    name: str
    jira_key: str
    description: str | None


class IssueInfoFromDB(BaseModel):
    id: int
    name: str
    project_id: int
    parent_issue_id: int | None
    type: str
    is_subtask: bool
    status: str
    limit_date: dt.date | None
    description: str | None
    update_timestamp: dt.datetime
    create_timestamp: dt.datetime


class SubtaskWithParents(BaseModel):
    subtask_id: int
    subtask_type: str
    subtask_name: str
    subtask_status: str
    limit_date: dt.date | None
    description: str | None
    project_id: int
    project_name: str
    issue_id_1: int
    issue_type_1: str
    issue_name_1: str
    issue_id_2: int
    issue_type_2: str
    issue_name_2: str
    update_timestamp: dt.datetime
    create_timestamp: dt.datetime


class SubtaskWithPath(BaseModel):
    id: int
    name: str
    project_id: int
    parent_issue_id: int | None
    type: str
    status: str
    limit_date: dt.date | None
    description: str | None
    update_timestamp: dt.datetime
    create_timestamp: dt.datetime
    path: str
