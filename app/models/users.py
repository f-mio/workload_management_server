# 標準モジュール
import datetime as dt
# サードパーティ製モジュール
from pydantic import BaseModel



class LoginForm(BaseModel):
    email: str
    password: str


class UserInfo(BaseModel):
    id: int
    name: str
    family_name: str
    first_name: str
    email: str
    hashed_password: str
    is_superuser: bool
    update_timestamp: dt.datetime
    create_timestamp: dt.datetime


class UserFormBody(BaseModel):
    name: str
    family_name: str
    first_name: str
    email: str
    password: str
