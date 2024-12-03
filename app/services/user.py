# サードパーティ製モジュール
from argon2 import PasswordHasher

# ref
#   - https://argon2-cffi.readthedocs.io/en/stable/

# インスタンス化
ph = PasswordHasher()


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
    is_correct_password: bool = ph.verify(hashed_password, password)
    return is_correct_password
