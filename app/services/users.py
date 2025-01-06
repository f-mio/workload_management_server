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
from services.auth import Auth_Utils

# ref
#   - https://argon2-cffi.readthedocs.io/en/stable/

# パスワードハッシャーのインスタンス化
ph = PasswordHasher()
# Auth_Utilsのインスタンス化
auth = Auth_Utils()

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


def insert_new_user_into_app_db(user_info: dict) -> list[dict, str]:
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
    jwt_token: str
        JWT Token

    Exceptions
    ----------
    - 登録済みのemailが存在する場合
    - [TODO] パスワードが脆弱な場合
    """
    # 必要情報の取り出し
    name = user_info.get("name")
    email = user_info.get("email")

    # name, emailがNoneでないことを確認する
    if (name is None) or name =="":
        raise ValueError("nameが入力されていません。")
    if (email is None) or email =="":
        raise ValueError("emailが入力されていません。")

    # emailが登録済みかどうかを判定する
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()
    stmt = select(User.id).where(User.email == email)
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

    # 管理者が0人だった場合に、新規ユーザを管理者にする。
    select_superuser_stmt = select(User.id).where(User.is_superuser == True)
    try:
        root_users = session.execute(select_superuser_stmt)
        session.close()
    except Exception as e:
        session.close()
        raise Exception(e)
    is_superuser: bool = True if root_users is None else False

    # 登録用ユーザ情報の作成
    new_user = {**user_info, "hashed_password": hashed_password,
                "is_superuser": is_superuser, "update_timestamp": dt.datetime.now(),}
    insert_stmt = insert(User).values(new_user)
    try:
        # ユーザ登録
        session.execute(insert_stmt)
        session.commit()
        session.close()
    except Exception as e:
        session.close()
        raise Exception(f"ユーザ登録に失敗しました。\nerror message: {e}")

    res_message = {"message": "ユーザ登録に成功しました"}

    jwt_token = auth.encode_jwt(email)

    return res_message, jwt_token


def verify_user_info_for_login(email: str, password: str) -> list[dict, str]:
    """
    ログイン処理

    Attributes
    ----------
    email: str
    password: str

    Returns
    -------
    message: dict
        サインアップ処理の成功失敗をメッセージで返却する。 (key: message)
    jwt_token: str
        JWT Token

    Exceptions
    ----------
    - DBからのデータ取得に失敗した場合
    - emailが存在しない場合
    - 認証情報が間違っていた場合
    - 無効なアカウントでログインした場合
    """
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()
    stmt = select(User.id, User.email, User.name,
                  User.first_name, User.family_name,
                  User.update_timestamp, User.create_timestamp,
                  User.is_active, User.hashed_password,)\
            .where(User.email == email)
    try:
        res_from_db = session.execute(stmt).first()
    except Exception as e:
        session.close()
        raise Exception("ログイン処理に失敗しました。")

    if res_from_db is None:
        raise Exception("登録されていないemailです")

    # パスワードの検証 & 有効ユーザの確認
    hashed_password = res_from_db.hashed_password
    is_correct_pass = verify_password_and_hashed_one(hashed_password, password)
    is_active = res_from_db.is_active
    if not is_correct_pass:
        raise Exception("パスワードが違います。")
    elif not is_active:
        raise Exception("アカウントが無効になっているためログインできません。")

    # レスポンス用データ
    user_info = {"id": res_from_db.id, "name": res_from_db.name, "email": res_from_db.email,
                "first_name": res_from_db.first_name, "family_name": res_from_db.family_name,
                "create_timestamp": res_from_db.create_timestamp, "update_timestamp": res_from_db.update_timestamp, }

    jwt_token = auth.encode_jwt(res_from_db.email)
    return user_info, jwt_token


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


def fetch_user_using_specify_email(email: str):
    """
    指定したemailアドレスを持つユーザ情報を取得する。

    Attributes
    ----------
    email: str
        emailアドレス

    Returns
    -------
    users: dict
        ユーザ情報

    Exceptions
    ----------
    - DBからのデータ取得に失敗した場合
    """
    stmt = select(
                User.id, User.name, User.first_name, User.family_name,
                User.email, User.update_timestamp, User.create_timestamp)\
            .where(User.email == email)
    Session = sessionmaker(bind=workload_db_engine)
    session = Session()

    try:
        res_from_db = session.execute(stmt).first()
        session.close()
        # ユーザが存在しない場合はエラー発報
    except Exception as e:
        session.close()
        raise Exception(e)

    if res_from_db is None:
        raise Exception("このemailは登録されていません。")
    # ユーザ情報の取得
    user_info = {"id": res_from_db.id, "name": res_from_db.name, "family_name": res_from_db.family_name,
                "first_name": res_from_db.first_name, "email": res_from_db.email,
                "create_timestamp": res_from_db.create_timestamp, "update_timestamp": res_from_db.update_timestamp, }
    return user_info
