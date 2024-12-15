# 標準モジュール
import datetime as dt
# サードパーティ製モジュール
from pydantic import BaseModel


class ProjectInfoFromDB(BaseModel):
    id: int
    name: str
    jira_key: str
    description: str
    is_target: bool # root userしか変更できない機能
    update_timestamp: dt.datetime
    create_timestamp: dt.datetime


class ProjectInfoFromJira(BaseModel):
    id: int
    name: str
    jira_key: str
    description: str


class ProjectForm(BaseModel):
    id: int
    name: str
    jira_key: str
    description: str | None

class Response_Message(BaseModel):
    message: str
