# 標準モジュール
import os
# サードパーティ製モジュール
from dotenv import load_dotenv
from pydantic import BaseModel

# .env記載情報をロード
load_dotenv()


class CsrfSettings(BaseModel):
    """
    csrf-protectのモデル設定
    """
    secret_key: str  = f"{os.getenv('SECRET_KEY_FOR_CSRF_TOKEN')}"


class CsrfType(BaseModel):
    """
    CSRFトークン
    """
    csrf_token: str

 
class ResponseMessage(BaseModel):
    message: str
