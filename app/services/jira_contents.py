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
from db.models import Project, Issue, SubtaskWithPathView


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

    # DB内のProjectから取込対象かどうかの情報を取得
    projects_in_db = fetch_all_projects_from_db()
    id2target_map = {
        str(p["id"]): ( p.get("is_target") if p.get("is_target") else False )
        for p in projects_in_db }

    # APIからのデータ取得とデータのデコード
    response = requests.request(
        "GET", jira_endpoint, headers=headers, auth=auth )
    decoded_res = json.loads(response.text)
    # レスポンスから必要な情報を抽出して、規定のフォーマットに直す
    projects = [
        { "id": str(project["id"]), "name": project["name"], "jira_key": project["key"],
          "description": project.get("description"),
          "is_target": (id2target_map.get(project["id"]) if id2target_map.get(project["id"]) else False)
        }
        for project in decoded_res ]

    return projects


def put_jira_target_status(project):
    """
    projectをDBにupsertする。update行う場合は、is_targetとupdate_timestampを更新する。

    Attributes
    ----------
    project: dict

    Returns
    -------
    None
    """
    # セッションの作成
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()

    # 登録用のSQL作成 (https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#insert-on-conflict-upsert)
    insert_stmt = insert(Project).values(project)
    upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['id'],
            set_= { "is_target": insert_stmt.excluded.is_target,
                    "update_timestamp": dt.datetime.now() }
    )
    # DBへの登録処理
    try:
        session.execute(upsert_stmt)
        session.commit()
        session.close()
        return { "message": "projectの更新に成功しました" }
    except Exception as e:
        session.close()
        raise Exception(e)


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
        projects = [
            { "id": info[0].id, "name": info[0].name, "jira_key": info[0].jira_key,
              "description": info[0].description, "is_target": info[0].is_target,
              "update_timestamp": info[0].update_timestamp,
              "create_timestamp": info[0].create_timestamp }
            for info in projects_raw ]
        return projects
    except Exception as e:
        session.close()
        raise Exception(e)


def generate_projects_for_upsert() -> list[dict]:
    """
    DB内のJIRA情報全更新のためのlist[dict]のproject情報を作成する。

    Attributes
    ----------
    None

    Returns
    -------
    projects: list[dict]
        更新対象のプロジェクト情報
    """
    # DBから有効projectを取得
    projects_from_db = fetch_all_projects_from_db()
    # Jiraから有効プロジェクト取得
    auth = HTTPBasicAuth(jira_user, jira_api_token)
    headers = { "Accept": "application/json" }
    # レスポンス格納用リスト
    projects = []

    # DB内の有効projectを走査 (is_target等の情報を格納するため)
    for project_in_db in projects_from_db:
        # 有効なIDを取得し、エンドポイントへ値を設定
        target_id = project_in_db["id"]
        jira_endpoint = f"{jira_base_url}/rest/api/3/project/{target_id}?expand=description,projectKeys"

        # APIからのデータ取得とデータのデコード
        response = requests.request(
            "GET", jira_endpoint, headers=headers, auth=auth )
        decoded_res = json.loads(response.text)

        project = {
            "id": decoded_res.get("id"), "name": decoded_res.get("name"),
            "jira_key": decoded_res.get("key"),
            "description": decoded_res.get("description"),
            "is_target": project_in_db["is_target"],
            "update_timestamp": dt.datetime.now()
        }
        project["description"] = modify_description_format(project["description"])

        # レスポンスリストに追加
        projects.append(project)

    return projects


def upsert_jira_project_info_into_db(project_info: dict | list[dict]) -> bool:
    """
    project情報をDBにupsertする。

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
    insert_stmt = insert(Project).values(project_info)
    upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['id'],
            set_= { "name": insert_stmt.excluded.name,
                    "jira_key": insert_stmt.excluded.jira_key,
                    "description": insert_stmt.excluded.description,
                    "is_target": insert_stmt.excluded.is_target,
                    "update_timestamp": dt.datetime.now() }
    )
    # DBへの登録処理
    try:
        session.execute(upsert_stmt)
        session.commit()
        session.close()
        return {"message": "projectの登録に成功しました"}
    except Exception as e:
        session.close()
        raise Exception(e)


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
    # API Endpoint  -->  https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-jql-get
    auth = HTTPBasicAuth(jira_user, jira_api_token)
    api_endpoint = f"{jira_base_url}/rest/api/3/search/jql"

    # 各project idを走査してissue, subtaskを振り分け
    for project_id in project_ids:
        # Jira JQLクエリパラメータ
        fields = "project,parent,status,created,assignee,status,summary,worklog,description,issuetype,duedate"
        params = { "jql": f"project={project_id}", "fields": fields,
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
            issue_name = issue["fields"].get("summary")
            issue_id = issue.get("id", None)
            issue_type = issue["fields"]["issuetype"]["name"]
            issue_description = str(issue["fields"].get("description")) \
                if issue["fields"].get("description") is not None \
                else ""
            issue_status = issue["fields"]["status"].get("name", "")
            issue_limit_date = issue["fields"].get("duedate")
            project_id = issue["fields"]["project"].get("id", None) \
                if ( issue["fields"].get("project") is not None ) \
                else None
            parent_id = issue["fields"]["parent"]["id"] \
                if ( issue["fields"].get("parent") is not None) \
                else None
            is_subtask = issue["fields"]["issuetype"]["subtask"]
            # issue_key = issue.get("key", None)
            # dict型のdescriptionフォーマット修正
            issue_description = modify_description_format(issue_description)
            # レスポンス用にissueを追加
            issues.append({
                "id": issue_id, "name": issue_name,
                "project_id": project_id, "parent_issue_id": parent_id,
                "type": issue_type, "is_subtask": is_subtask,
                "status": issue_status, "limit_date": issue_limit_date,
                "description": issue_description,
                "update_timestamp": dt.datetime.now(),
            })

    return issues


def modify_description_format(description):
    try:
        description_dict = json.loads(description.replace("'", '"'))
        if (isinstance(description_dict, dict)):
            new_description = ""
            for idx, content in enumerate(description_dict.get("content", [])):
                if idx > 0:
                    new_description += "\n"
                if isinstance(content, dict):
                    for inner_content in content.get("content", []):
                        new_description += inner_content["text"]
                else:
                    new_description += content
        else:
            new_description = str(description)
    except Exception:
        return description
    
    return new_description


def upsert_jira_issues_into_app_db(issues: list[dict]):
    """
    DBに登録されているprojectを取得してDB内のissuesを更新する。

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
    insert_stmt = insert(Issue).values(issues)
    # idが競合した場合はnameとupdate_timestampを更新 (https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Insert.excluded)
    upsert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=['id'],
        set_={ "name": insert_stmt.excluded.name,
               "project_id": insert_stmt.excluded.project_id,
               "parent_issue_id": insert_stmt.excluded.parent_issue_id,
               "type": insert_stmt.excluded.type,
               "status": insert_stmt.excluded.status,
               "limit_date": insert_stmt.excluded.limit_date,
               "description": insert_stmt.excluded.description,
               "update_timestamp": dt.datetime.now() }
    )
    try:
        session.execute(upsert_stmt)
        session.commit()
        session.close()
    except Exception as e:
        session.close()
        raise Exception(e)


def fetch_all_main_issues_from_db() -> list[dict]:
    """
    DBに登録されているsubtask以外のissueを取得して返却する。

    Attributes
    ----------
    None

    Returns
    -------
    projects: list[dict]
        key: id, name, project_id, parent_issue_id, type,
             is_subtask, status, limit_date, description,
             update_timestamp, create_timestamp
    """
    # セッションの作成
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()
    # 取得用のSQL作成
    stmt = select(Issue).where(Issue.is_subtask == False)\
            .order_by(Issue.project_id, Issue.parent_issue_id, Issue.id)
    try:
        # DBからのデータ取得
        issues_raw = session.execute(stmt).all()
        session.close()
        # データの成形
        issues = [
            { "id": info[0].id, "name": info[0].name, "project_id": info[0].project_id,
              "parent_issue_id": info[0].parent_issue_id, "type": info[0].type,
              "is_subtask": info[0].is_subtask, "status": info[0].status,
              "limit_date": info[0].limit_date, "description": info[0].description,
              "update_timestamp": info[0].update_timestamp,
              "create_timestamp": info[0].create_timestamp }
            for info in issues_raw ]

        return issues
    except Exception as e:
        session.close()
        raise Exception(e)


def fetch_all_subtasks_from_db() -> list[dict]:
    """
    DBに登録されているsubtaskを取得して返却する。

    Attributes
    ----------
    None

    Returns
    -------
    projects: list[dict]
        key: id, name, project_id, parent_issue_id, type,
             is_subtask, status, limit_date, description,
             update_timestamp, create_timestamp
    """
    # セッションの作成
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()
    # 取得用のSQL作成
    stmt = select(Issue).where(Issue.is_subtask == True)\
            .order_by(Issue.project_id, Issue.parent_issue_id, Issue.id)
    try:
        # DBからのデータ取得
        subtasks_raw = session.execute(stmt).all()
        session.close()
        # データの成形
        subtasks = [
            { "id": info[0].id, "name": info[0].name, "project_id": info[0].project_id,
              "parent_issue_id": info[0].parent_issue_id, "type": info[0].type,
              "is_subtask": info[0].is_subtask, "status": info[0].status,
              "limit_date": info[0].limit_date, "description": info[0].description,
              "update_timestamp": info[0].update_timestamp,
              "create_timestamp": info[0].create_timestamp }
            for info in subtasks_raw ]

        return subtasks
    except Exception as e:
        session.close()
        raise Exception(e)


def fetch_all_subtasks_with_path_from_db():
    """
    DBに登録されているsubtaskを取得して返却する。

    Attributes
    ----------
    None

    Returns
    -------
    projects: list[dict]
        key: id, name, project_id, parent_issue_id, type,
             is_subtask, status, limit_date, description,
             update_timestamp, create_timestamp
    """
    # セッションの作成
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()
    # 取得用のSQL作成
    stmt = select(
                SubtaskWithPathView.id, SubtaskWithPathView.name, SubtaskWithPathView.project_id,
                SubtaskWithPathView.parent_issue_id, SubtaskWithPathView.type, SubtaskWithPathView.is_subtask,
                SubtaskWithPathView.status, SubtaskWithPathView.limit_date, SubtaskWithPathView.description,
                SubtaskWithPathView.path, SubtaskWithPathView.update_timestamp, SubtaskWithPathView.create_timestamp )\
            .order_by(
                SubtaskWithPathView.project_id, SubtaskWithPathView.parent_issue_id, SubtaskWithPathView.id)

    try:
        # DBからのデータ取得
        res = session.execute(stmt).all()
        session.close()
        # データの成形
        subtasks = [
            { "id": info.id, "name": info.name, "project_id": info.project_id,
              "parent_issue_id": info.parent_issue_id, "type": info.type,
              "is_subtask": info.is_subtask, "status": info.status,
              "limit_date": info.limit_date, "description": info.description,
              "path": info.path,
              "update_timestamp": info.update_timestamp,
              "create_timestamp": info.create_timestamp }
            for info in res ]

        return subtasks
    except Exception as e:
        session.close()
        raise Exception(e)
