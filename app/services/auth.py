
# 標準モジュール
import os
import datetime as dt
# サードパーティ製モジュール
from dotenv import load_dotenv
import jwt
# プロジェクトモジュール
from services.custom_exceptions import JwtTokenError

# 環境変数の読み込み
load_dotenv()

# シークレットキーのロード
SECRET_KEY_JWT_TOKEN = f'{os.getenv("SECRET_KEY_FOR_JWT_TOKEN")}'
SECRET_KEY_CSRF_TOKEN = f'{os.getenv("SECRET_KEY_FOR_CSRF_TOKEN")}'
# JWT有効時間の設定
JWT_EXPIRE_MINUTE = 60

class Auth_Utils():
    """
    JWT, CSRF tokenの認証関係メソッドを格納したクラス
        - https://pyjwt.readthedocs.io/en/stable/api.html
        - https://github.com/aekasitt/fastapi-csrf-protect/tree/master
    """

    def encode_jwt(self, user_id) -> str:
        """
        jwt
        """
        payload: dict = {
            "exp": dt.datetime.now(tz=dt.timezone.utc) + dt.timedelta(days=0, minutes=JWT_EXPIRE_MINUTE),
            "iat": dt.datetime.now(tz=dt.timezone.utc),
            "sub": str(user_id)
        }
        return jwt.encode(payload, SECRET_KEY_JWT_TOKEN, algorithm="HS256")


    def decode_jwt(self, token) -> str:
        """
        jwtトークンをデコードし、適切なものだった場合subキーに格納されている文字列(user_id)を返す。
        """
        try:
            payload = jwt.decode(token, SECRET_KEY_JWT_TOKEN, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise JwtTokenError(
                status_code=401, detail="JWTトークンの有効期限切れです。")
        except jwt.InvalidTokenError as e:
            raise JwtTokenError(status_code=401, detail=f"不正なJWTトークンです。\nError message: {e}")


    def verify_jwt(self, request) -> int:
        """
        jwtトークンを検証し、適切な場合emailを返す。
        """
        access_token = request.cookies.get("access_token")
        if not access_token:
            raise JwtTokenError(
                status_code=401, detail='No JWT exist: may not set yet or deleted')
        _, _, jwt_token = access_token.partition(" ")
        user_id = self.decode_jwt(jwt_token)
        return int(user_id)


    def verify_update_jwt(self, request) -> tuple[str, str]:
        """
        JWTトークンの検証と更新を行い、新しいtokenとsubject(id)を返却する。
        """
        subject = self.verify_jwt(request)
        new_token = self.encode_jwt(subject)
        return new_token, subject


    def verify_csrf_update_jwt(self, request, csrf_protect, headers) -> str:
        """
        CSRFトークン検証およびJWTトークンの検証を行い、新しいJWT tokenを返却する。
        """
        csrf_token = csrf_protect.get_csrf_from_headers(headers)
        csrf_protect.validate_csrf(csrf_token)
        subject = self.verify_jwt(request)
        new_token = self.encode_jwt(subject)
        return new_token
