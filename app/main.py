# 標準モジュール
import os
# サードパーティ製モジュール
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from argon2.exceptions import VerifyMismatchError
import uvicorn
# プロジェクトモジュール
from api.current import (
    auth, users, projects, issues, workloads)
from models.auth import CsrfSettings
from services.custom_exceptions import LoginError, SignupError, JwtTokenError


# .env記載情報をロード
load_dotenv()

# csrf-protect設定
@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()
# CORS設定
CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']

# routerの読み込み
auth_router = auth.router
user_router = users.router
project_router = projects.router
issue_router = issues.router
workload_router = workloads.router

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
app.include_router(issue_router)
app.include_router(workload_router)


# Exception Handler
@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

@app.exception_handler(VerifyMismatchError)
async def login_mismatch_pass_exception_handler(request: Request, exc: VerifyMismatchError):
    return JSONResponse(
        status_code=403,
        content={"message": f"ログイン失敗しました。\nError message: {str(exc)}"},)

@app.exception_handler(LoginError)
async def login_exception_handler(request: Request, exc: LoginError):
    return JSONResponse(
        status_code=403,
        content={"message": f"ログイン失敗しました。\nError message: {str(exc)}"},)

@app.exception_handler(SignupError)
async def signup_exception_handler(request: Request, exc: SignupError):
    return JSONResponse(
        status_code=403,
        content={"message": f"アカウント作成に失敗しました。\nError message: {str(exc)}"},)

@app.exception_handler(JwtTokenError)
async def jwt_exception_handler(request: Request, exc: JwtTokenError):
    return JSONResponse(
        status_code=403,
        content={"message": f"Error message: {str(exc)}"},)

@app.exception_handler(Exception)
async def signup_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=401,
        content={"message": f"エラーが発生しました。\nError message: {str(exc)}"},)




# メイン処理の場合はuvicornを立ち上げる。 ref: https://www.uvicorn.org/#running-programmatically
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv('FAST_API_HOST'), port=8000,
        reload=True
    )
