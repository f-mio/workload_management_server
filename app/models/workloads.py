# 標準モジュール
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
