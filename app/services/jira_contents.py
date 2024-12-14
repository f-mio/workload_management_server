# 標準モジュール
import os
import json
import requests
from requests.auth import HTTPBasicAuth
# サードパーティ製モジュール
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# 環境変数からJIRAのAPIへのアクセス情報を取得
jira_base_url = os.environ["JIRA_BASE_URL"]
jira_user = os.environ["JIRA_MANAGER_EMAIL"]
jira_api_token = os.environ["JIRA_WORKLOAD_API_TOKEN"]


def fetch_all_projects_from_jira() -> list[dict | None]:
    """
    JiraからAPIユーザの権限で取得できる全てのプロジェクトを取得して表示する。

    Attributes
    ----------
    None

    Returns
    -------
    projects: list[dict]
        key: id, name, jira_key, description
    """
    # APIアクセス用情報の宣言
    auth = HTTPBasicAuth(jira_user, jira_api_token)
    headers = { "Accept": "application/json" }
    jira_endpoint = f"{jira_base_url}/rest/api/3/project?expand=description"
    # APIからのデータ取得とデータのデコード
    response = requests.request(
        "GET", jira_endpoint, headers=headers, auth=auth )
    decoded_res = json.loads(response.text)
    # レスポンスから必要な情報を抽出して、規定のフォーマットに直す
    projects = [
        { "id": project["id"], "name": project["name"], "jira_key": project["key"],
        "description": project.get("description") }
        for project in decoded_res ]

    return projects


def fetch_all_projects_from_db() -> list[dict | None]:
    """
    DBに登録されているprojectを取得して返却する。

    Attributes
    ----------
    None

    Returns
    -------
    projects: list[dict]
        key: id, name, jira_key, description, is_target
    """
    pass


def register_project_info_to_db(project_info: dict) -> bool:
    """
    DBに登録されているprojectを取得して返却する。

    Attributes
    ----------
    None

    Returns
    -------
    project_info: dict
        key: id, name, jira_key, description, is_target
    """

    aaa = ""

    try:
        # 登録処理

        return True

    except Exception as e:
        return False
