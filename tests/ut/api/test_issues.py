from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_should_fetch_all_issues():
    """
    /issues/へアクセスすれば全てのissueを取得できることを確認。
    """
    pass

