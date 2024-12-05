# 標準モジュール
import os
# サードパーティ製モジュール
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette_csrf import CSRFMiddleware

# .env記載情報をロード
load_dotenv()

# FastAPIインスタンス
app = FastAPI()

app.add_middleware(CSRFMiddleware, secret=os.getenv('SECRET_KEY_FOR_CSRF_TOKEN'))

# [TODO] デモ
@app.get("/")
def demo():
    return {"message": "Hello, FastAPI"}


# メイン処理の場合はuvicornを立ち上げる。 ref: https://www.uvicorn.org/#running-programmatically
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv('FAST_API_HOST'), port=8000,
        reload=True
    )
