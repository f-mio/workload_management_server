# 標準モジュール
import os
import re
import json
import requests
import datetime as dt
from requests.auth import HTTPBasicAuth
# サードパーティ製モジュール
from sqlalchemy import create_engine, select, update, and_, delete
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.dialects.postgresql import insert
# プロジェクトモジュール
from db.models import Workload, SubtaskWithPathView, Project, Issue, User
from models.auth import ResponseMessage

# SQLAlchemyのエンジン
workload_db_engine = create_engine(os.environ["WORKLOAD_DATABASE_URI"])


def insert_workload_info_into_db(workload_info: dict) -> dict:
    """
    フォームに入力されたworkloadをDBに登録する。

    Attributes
    ----------
    workload_info: dict

    Returns
    -------
    message: dict (key: message)

    Exception
    ---------
    - DB接続失敗
    - JIRAからの情報取得失敗
    """
    # セッションの作成
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()

    # 登録用のSQL作成
    insert_stmt = insert(Workload).values(workload_info)
    # DBへの登録処理
    try:
        session.execute(insert_stmt)
        session.commit()
        session.close()
        return {"message": "工数登録に成功しました"}
    except Exception as e:
        session.close()
        raise Exception(e)


def fetch_specify_workload(workload_id: int) -> dict:
    """
    指定されたIDの工数情報を取得する。

    Attributes
    ----------
    workload_id: int
        工数登録情報ID

    Returns
    -------
    workload: dict
        ID指定した工数情報

    Exception
    ---------
    - DB接続失敗
    """
    # セッションの作成
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()
    stmt = select(Workload).\
            where(Workload.id == workload_id)

    try:
        workload_obj = session.execute(stmt).first()

        # IDが存在しない場合
        if workload_obj is None:
            raise Exception("無効な工数情報IDが指定されました。")

        workload = { "id": workload_obj[0].id,
                     "subtask_id": workload_obj[0].subtask_id,
                     "user_id": workload_obj[0].user_id,
                     "work_date": workload_obj[0].work_date,
                     "workload_minute": workload_obj[0].workload_minute,
                     "detail": workload_obj[0].detail,
                     "update_timestamp": workload_obj[0].update_timestamp,
                     "create_timestamp": workload_obj[0].create_timestamp, }
        session.close()
        return workload
    except Exception as e:
        session.close()
        raise Exception(e)


def update_specify_workload(workload_id: int , form_value: dict) -> dict:
    """
    指定したIDの工数情報をフォームで登録した内容で修正する。

    Attributes
    ----------
    workload_id: int
        登録済み工数情報のID
    form_value: dict
        フォームで入力した修正内容

    Returns
    -------
    message: dict

    Exception
    ---------
    None
    """
    # セッションの作成
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()
    # 有効IDかどうかを確認するクエリ作成
    check_stmt = select(Workload.id).where(Workload.id == workload_id)
    # 更新用クエリ作成
    update_stmt = update(Workload)\
            .where(Workload.id == workload_id)\
            .values( subtask_id = form_value["subtask_id"],
                     user_id = form_value["user_id"],
                     work_date = form_value["work_date"],
                     workload_minute = form_value["workload_minute"],
                     detail = form_value["detail"],
                     update_timestamp = dt.datetime.now() )

    try:
        # 存在するIDかどうかを確認。
        check_data = session.execute(check_stmt).first()
        if check_data is None:
            raise Exception(f"工数情報ID {workload_id}は登録されていません。\nIDを確認してください。")
        # updateの実行
        session.execute(update_stmt)
        session.commit()
        session.close()
        return {"message": "工数情報を修正しました。"}
    except Exception as e:
        session.close()
        return {"message": f"工数情報修正に失敗しました。\nerror message: {e}"}


def delete_workload(workload_id: int, user_id: int):
    """
    指定されたIDの工数を削除する機能 (所有者か、管理者でないと削除できない)

    Attributes
    ----------
    workload_id: int
        登録済み工数情報のID
    user_id: int
        JWTから入手したユーザID

    Returns
    -------
    message: dict

    """
    # セッション作成
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()

    # ユーザ取得
    user_stmt = select(User.id, User.is_superuser).where(User.id == user_id)
    try:
        # DBからデータを取得
        user_obj = session.execute(user_stmt).first()
        # IDが存在しない場合
        if user_obj is None:
            raise Exception("無効なユーザIDが指定されました。")
        # ユーザIDの取得
        user_info = { "id": user_obj.id, "is_superuser": user_obj.is_superuser }
    except Exception as e:
        session.close()
        raise Exception(e)

    # 工数取得
    workload_stmt = select(Workload.id, Workload.user_id)\
                        .where(Workload.id == workload_id)

    try:
        # DBからデータを取得
        workload_obj = session.execute(workload_stmt).first()
        # IDが存在しない場合
        if workload_obj is None:
            raise Exception("無効な工数情報IDが指定されました。")
        # idとuser_idのみを取得
        workload = { "id": workload_obj.id,
                     "user_id": workload_obj.user_id }
    except Exception as e:
        raise Exception(e)

    # 対象工数が自身が所有もしくはユーザが管理者でなければ、削除できないというメッセージを返却
    if not (user_info["is_superuser"] or workload.user_id == user_id):
        return {"message": "削除に失敗しました。\n所有者または管理者でない場合削除できません。"}

    # 削除処理
    del_stmt = delete(Workload).where(Workload.id == workload["id"])

    try:
        session.execute(del_stmt)
        session.commit()
    except Exception as e:
        session.close()
        raise Exception(e)

    # セッションの終了
    session.close()

    return {"message": "削除にしました。"}


def fetch_specify_condition_workloads_from_db(condition: dict) -> list[dict]:
    """
    指定条件の登録済み工数をを取得

    Attributes
    ----------
    condition: dict
        条件

    Returns
    -------
    workloads: list[dict]
        指定条件の工数

    Exception
    ---------
    - DB接続失敗
    """

    Session = sessionmaker(bind=workload_db_engine)
    session = Session()

    # エイリアスを関数内で定義
    ParentIssue = aliased(Issue)
    ChildIssue = aliased(Issue)

    res = session.query(Workload, SubtaskWithPathView, Project, ParentIssue, ChildIssue, User)\
        .join(SubtaskWithPathView, SubtaskWithPathView.id == Workload.subtask_id, isouter=True)\
        .join(Project, Project.id == SubtaskWithPathView.project_id, isouter=True)\
        .join(ParentIssue, and_(SubtaskWithPathView.path.contains(ParentIssue.id), ParentIssue.parent_issue_id.is_(None) ), isouter=True)\
        .join(ChildIssue, and_(SubtaskWithPathView.path.contains(ChildIssue.id), ChildIssue.parent_issue_id == ParentIssue.id), isouter=True)\
        .join(User, Workload.user_id == User.id)\
        .order_by(Workload.work_date, Project.id, ParentIssue.id, ChildIssue.id, SubtaskWithPathView.id, Workload.id)

    target_date = condition.get("target_date")
    lower_date = condition.get("lower_date")
    upper_date = condition.get("upper_date")
    user_id = condition.get("specify_user_id")
    workload_id = condition.get("workload_id")
    is_target_project = condition.get("is_target_project")

    if target_date is not None:
        res = res.filter(Workload.work_date == target_date)
    if lower_date is not None:
        res = res.filter(Workload.work_date >= lower_date)
    if upper_date is not None:
        res = res.filter(Workload.work_date <= upper_date)
    if user_id is not None:
        res = res.filter(Workload.user_id == int(user_id))
    if workload_id is not None:
        res = res.filter(Workload.id == int(workload_id))
    if is_target_project is not None:
        res = res.filter(Project.is_target == is_target_project)

    workloads = [ { "project_id": info[2].id,
                    "project_name": info[2].name,
                    "path": info[1].path,
                    "issue_id_1": info[3].id if info[3] else None,
                    "issue_name_1": info[3].name if info[3] else None,
                    "issue_id_2": info[4].id if info[4] else None,
                    "issue_name_2": info[4].name if info[4] else None,
                    "subtask_id": info[0].subtask_id if info[0] else None,
                    "subtask_name": info[1].name if info[1] else None,
                    "workload_id": info[0].id,
                    "user_id": info[0].user_id, "user_name": info[5].name,
                    "work_date": info[0].work_date,
                    "workload_minute": info[0].workload_minute,
                    "detail": info[0].detail,
                    "update_timestamp": info[0].update_timestamp,
                    "create_timestamp": info[0].create_timestamp
                  } for info in res.all()
                ]

    return workloads
