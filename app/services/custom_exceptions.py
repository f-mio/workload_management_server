
class LoginError(Exception):
    """
    ログイン失敗時のカスタムException
    """
    pass


class SignupError(Exception):
    """
    サインイン失敗時のカスタムException
    """
    pass


class JwtTokenError(Exception):
    """
    JWTトークンに関わるException
    """
    pass
