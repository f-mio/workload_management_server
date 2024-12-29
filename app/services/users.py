# 標準モジュール
import os
import datetime as dt
# サードパーティ製モジュール
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
# プロジェクトモジュール
from db.models import User

# ref
#   - https://argon2-cffi.readthedocs.io/en/stable/

# パスワードハッシャーのインスタンス化
ph = PasswordHasher()

# sql alchemyのエンジン作成
workload_db_engine = create_engine(os.environ["WORKLOAD_DATABASE_URI"])


def convert_password_to_hashed_one(password: str) -> str:
    """
    パスワードをハッシュ化パスワードに変更する

    Attributes
    ----------
    password: str
        ハッシュ化対象のパスワード

    returns
    -------
    hashed_password: str
        ハッシュ化後パスワード

    Exception
    ---------
    None
    """
    hashed_password: str = ph.hash(password)
    return hashed_password


def verify_password_and_hashed_one(hashed_password: str, password: str) -> bool:
    """
    ハッシュ化したパスワードとパスワードを比較し、正しいものの場合Trueを返す。
    正しくないものの場合はFalseを返す。
    Attributes
    ----------
    password: str
        パスワード
    hashed_password: str
        ハッシュ化パスワード

    returns
    -------
    is_correct_password: bool
        ハッシュ化パスワードとパスワードの検証結果

    Exception
    ---------
    None
    """
    try:
        is_correct_password: bool = ph.verify(hashed_password, password)
    except VerifyMismatchError:
        is_correct_password = False
    except InvalidHashError:
        is_correct_password = False
    except Exception as e:
        raise Exception(e)

    return is_correct_password


def insert_new_user_into_app_db(user_info: dict) -> dict:
    """
    ユーザ登録処理

    Attributes
    ----------
    user_info: dict
        key: name, family_name, first_name, email, password

    Returns
    -------
    message: dict
        サインアップ処理の成功失敗をメッセージで返却する。 (key: message)

    Exceptions
    ----------
    - 登録済みのemailが存在する場合
    - パスワードが脆弱な場合
    """
    # 必要情報の取り出し
    name = user_info.get("name")
    # family_name = user_info.get("family_name")
    # first_name = user_info.get("first_name")
    email = user_info.get("email")

    # name, emailがNoneでないことを確認する
    if (name is None) or name =="":
        raise ValueError("nameが入力されていません。")
    if (email is None) or email =="":
        raise ValueError("emailが入力されていません。")

    # emailが登録済みかどうかを判定する
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()
    stmt = select(User).where(User.email == email)
    try:
        any_user = session.execute(stmt).all()
    except Exception as e:
        session.close()
        raise Exception(f"ユーザ登録時のemail検証作業に失敗しました。\nerror message: {e}")

    if any_user:
        session.close()
        return { "message": f"このemailアドレス[{email}]はすでに登録されています。別のアドレスを使用してください。"}

    # パスワードの検証
    # [TODO] 脆弱性判定を行う

    # パスワードのハッシュ化
    password = user_info.pop("password")
    hashed_password: str = convert_password_to_hashed_one(password)
    # 登録用ユーザ情報の作成
    new_user = {**user_info, "hashed_password": hashed_password,
                "is_superuser": False, "update_timestamp": dt.datetime.now(),}
    stmt = insert(User).values(new_user)
    try:
        # ユーザ登録
        session.execute(stmt)
        session.commit()
        session.close()
    except Exception as e:
        session.close()
        raise Exception(f"ユーザ登録に失敗しました。\nerror message: {e}")

    res_message = {"message": "ユーザ登録に成功しました"}
    return res_message


def verify_user_info_for_login(email: str, password: str) -> str:
    """
    ログイン処理
    """
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()
    stmt = select(User).where(User.email == email)

    try:
        res_from_db = session.execute(stmt).first()
    except Exception as e:
        session.close()
        raise Exception("ログイン処理に失敗しました。")

    user_info = {"id": res_from_db[0].id, "name": res_from_db[0].name, "family_name": res_from_db[0].family_name,
                 "first_name": res_from_db[0].first_name, "email": res_from_db[0].email,
                 "hashed_password": res_from_db[0].hashed_password, "is_superuser": res_from_db[0].is_superuser,
                 "create_timestamp": res_from_db[0].create_timestamp, "update_timestamp": res_from_db[0].update_timestamp, }

    is_correct_pass = verify_password_and_hashed_one(user_info["hashed_password"], password)
    if not is_correct_pass:
        raise Exception("パスワードが違います。")

    return user_info


def fetch_active_user_list():
    """
    有効なユーザ一覧を返却する

    Attributes
    ----------
    None

    Returns
    -------
    users: list[dict]
        有効なユーザ情報

    Exceptions
    ----------
    - DBからのデータ取得に失敗した場合
    """
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()
    stmt = select(User.id, User.name)\
            .where(User.is_active == True)

    try:
        res = session.execute(stmt).all()
        users = [ {"id": user_res[0], "name": user_res[1]}
                for user_res in res]
        session.close()
        return users
    except Exception as e:
        session.close()
        raise Exception(e)
