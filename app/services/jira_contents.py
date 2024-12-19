# 標準モジュール
import os
import json
import requests
import datetime as dt
from requests.auth import HTTPBasicAuth
# サードパーティ製モジュール
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
# プロジェクトモジュール
from db.models import Project, Issue, Subtask


# 環境変数からJIRAのAPIへのアクセス情報を取得
jira_base_url = os.environ["JIRA_BASE_URL"]
jira_user = os.environ["JIRA_MANAGER_EMAIL"]
jira_api_token = os.environ["JIRA_WORKLOAD_API_TOKEN"]
# SQLAlchemyのエンジン
workload_db_engine = create_engine(os.environ["WORKLOAD_DATABASE_URI"])


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
    # セッションの作成
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()
    # project取得用のSQL作成 (https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#using-select-statements)
    stmt = select(Project).where(Project.is_target == True).order_by(Project.id)
    try:
        # DBからのデータ取得
        projects_raw = session.execute(stmt).all()
        session.close()
        # データの成形
        projects = [ { "id": info[0].id, "name": info[0].name, "jira_key": info[0].jira_key,
                       "description": info[0].description, "is_target": info[0].is_target,
                       "update_timestamp": info[0].update_timestamp,
                       "create_timestamp": info[0].create_timestamp }
                     for info in projects_raw ]
        return projects
    except Exception as e:
        session.close()
        raise Exception(e)


def upsert_project_info_into_db(project_info: dict) -> bool:
    """
    DBに登録されているprojectを取得して返却する。

    Attributes
    ----------
    None

    Returns
    -------
    message: str
        成功失敗のメッセージ。
    """
    # セッションの作成
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()
    # 登録用のSQL作成 (https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#insert-on-conflict-upsert)
    upsert_stmt = insert(Project).values(project_info)\
            .on_conflict_do_update(
                index_elements=['id'],
                set_= {
                    "name": project_info["name"],
                    "jira_key": project_info["jira_key"],
                    "description": project_info["description"],
                    "is_target": project_info["is_target"],
                    "update_timestamp": project_info["update_timestamp"],
            })
    # DBへの登録処理
    try:
        session.execute(upsert_stmt)
        session.commit()
        session.close()
        return {"message": "projectの登録に成功しました"}
    except Exception as e:
        session.close()
        return {"message": f"projectの登録に失敗しました。\nerror message: {e}"}

def fetch_all_issues_related_project_ids_from_jira(project_ids: list):
    """
    Project IDを用いてそれに紐づくissues, subtasksを取得して返却する。

    Attributes
    ----------
    project_ids

    Returns
    -------
    issues
    subtasks

    Exception
    ---------
    - DB接続失敗
    - JIRAからの情報取得失敗
    """
    # 結果格納用リスト
    issues = []
    subtasks = []
    # API Endpoint
    auth = HTTPBasicAuth(jira_user, jira_api_token)
    api_endpoint = f"{jira_base_url}/rest/api/3/search"


    for project_id in project_ids:
        # Jira JQLクエリパラメータ
        params = { "jql": f"project={project_id}",
                   "maxResults": 5000,  "startAt": 0, }
        # リクエストの送信
        response = requests.get(
            api_endpoint, headers={ "Accept": "application/json" },
            params=params, auth=auth )

        # レスポンスの確認
        if response.status_code != 200:
            continue

        issue_res = response.json().get("issues", [])
        if len(issue_res)==0:
            continue

        # responseを走査して適切なフォーマットでissueとsubtaskに振り分ける
        for issue in issue_res:
            issue_name = issue['fields']['summary']
            issue_id = issue.get("id", None)
            issue_key = issue.get("key", None)
            issue_type = issue["fields"]["issuetype"]["name"]
            issue_description = issue.["fields"].get("description", "")
            project_id = issue["fields"]["project"].get("id", None) \
                if ( issue["fields"].get("project") is not None ) \
                else None
            parent_id = issue["fields"]["parent"]["id"] \
                if ( issue["fields"].get("parent") is not None) \
                else None

            # # [[TODO]]
            # XXX_date = aaa \
            #     if ( aaa is not None)\
            #     else None

            # subtaskかどうかを判定
            is_subtask = issue["fields"]["issuetype"]["subtask"]
            if is_subtask:
                subtasks.append({
                    "id": issue_id, "jira_key": issue_key, "name": issue_name,
                    "type": issue_type, "parrent_issue_id": parent_id,
                    "project_id": project_id, "description": issue_description,
                    "update_timestamp": dt.datetime.now(),
                })
            else:
                # [[TODO]]
                issues.append({
                    "id": issue_id, "jira_key": issue_key,
                    "type": issue_type, "parrent_issue_id": parent_id,
                    "project_id": project_id, "description": issue_description,
                    "update_timestamp": dt.datetime.now(),
                })

    return [issues, subtasks]

