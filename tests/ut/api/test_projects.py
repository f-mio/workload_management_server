from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_should_fetch_projects():
    """
    /projects/へアクセスすれば設定で入力された全てのprojectを取得できることを確認。
    """
    pass
