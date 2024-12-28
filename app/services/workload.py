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
from db.models import Workload
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


def fetch_specify_user_workloads_from_db(
        user_id: int, lower_date: dt.date | None = None,
        upper_date: dt.date | None = None) -> list[dict]:
    """
    user_idに紐づく工数を取得

    Attributes
    ----------
    user_id: int
        ユーザID
    range_days: int
        本日から取得期間 (デフォルト値: 365日)
    upper_date: dt.date
        取得日時

    Returns
    -------
    workloads: list[dict]
        user_idが持つ工数情報

    Exception
    ---------
    - DB接続失敗
    """
    # 期間が未指定の場合365日を設定
    if lower_date is None:
        lower_date = dt.date.today() - dt.timedelta(days=365)
    if upper_date is None:
        upper_date = dt.date.today()

    Session = sessionmaker(bind=workload_db_engine)
    session = Session()

    stmt = select(Workload)\
            .where(
                Workload.user_id == user_id,
                Workload.work_date >= lower_date,
                Workload.work_date <= upper_date) \
            .order_by(Workload.work_date, Workload.id)
 
    try:
        db_res = session.execute(stmt).all()
        workloads = [ {"id": info[0].id,
                       "subtask_id": info[0].subtask_id, "user_id": info[0].user_id,
                       "work_date": info[0].work_date, "workload_minute": info[0].workload_minute,
                       "detail": info[0].detail,
                       "update_timestamp": info[0].update_timestamp, "create_timestamp": info[0].create_timestamp,
                      }
                      for info in db_res
                    ]
        session.close()
    except Exception as e:
        session.close()
        raise Exception(e)

    return workloads
