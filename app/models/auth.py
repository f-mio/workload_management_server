# 標準モジュール
import os
# サードパーティ製モジュール
from dotenv import load_dotenv
from pydantic import BaseModel

# .env記載情報をロード
load_dotenv()


# csrf-protectのモデル設定
class CsrfSettings(BaseModel):
    secret_key: str  = f"{os.getenv('SECRET_KEY_FOR_CSRF_TOKEN')}"


# CSRFトークン
class CsrfType(BaseModel):
    csrf_token: str

 
class ResponseMessage(BaseModel):
    message: str
