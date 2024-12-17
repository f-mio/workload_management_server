# 標準モジュール
import os
# サードパーティ製モジュール
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
import uvicorn
# プロジェクトモジュール
from api.current import auth, users, projects
from models.auth import CsrfSettings

# .env記載情報をロード
load_dotenv()

# csrf-protect設定
@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()
# CORS設定
CORS_ORIGINS = ['http://localhost:3000']

# routerの読み込み
auth_router = auth.router
user_router = users.router
project_router = projects.router

# FastAPIインスタンス
app = FastAPI()
app.add_middleware(
   CORSMiddleware,
   allow_origins=CORS_ORIGINS,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
  return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


# [TODO] デモ
@app.get("/")
def demo(request: Request, csrf_protect: CsrfProtect = Depends()):
    """
    """
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    return {"a": csrf_token, "b": signed_token}


# メイン処理の場合はuvicornを立ち上げる。 ref: https://www.uvicorn.org/#running-programmatically
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv('FAST_API_HOST'), port=8000,
        reload=True
    )
