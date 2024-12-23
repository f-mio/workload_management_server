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
