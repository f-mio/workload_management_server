# 標準モジュール
from typing import Optional
import datetime as dt
# サードパーティ製モジュール
from pydantic import BaseModel


class WorkloadInfoFromDB(BaseModel):
    id: int
    subtask_id: int
    user_id: int
    work_date: dt.date
    workload_minute: int
    detail: str
    update_timestamp: dt.datetime
    create_timestamp: dt.datetime


class WorkloadForm(BaseModel):
    subtask_id: int
    user_id: int
    work_date: dt.date
    workload_minute: int
    detail: str


class WorkloadCondition(BaseModel):
    specity_user_id: Optional[int] = None
    target_date: Optional[dt.date] = None
    lower_date: Optional[dt.date] = None
    upper_date: Optional[dt.date] = None
    # project_id: Optional[int] = None
    # issue_list: Optional[list] = None


class RegisteredWorkload(BaseModel):
    project_id: int
    project_name: str
    issue_id_1: int | None
    issue_name_1: str | None
    issue_id_2: int | None
    issue_name_2: str | None
    subtask_id: int
    subtask_name: str
    workload_id: int
    user_id: int
    user_name: str
    work_date: dt.date
    workload_minute: int
    detail: str
    update_timestamp: dt.datetime
    create_timestamp: dt.datetime
