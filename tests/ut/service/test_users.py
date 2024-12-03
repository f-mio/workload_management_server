# サードバーティ製モジュール
import pytest
# プロジェクトモジュール
from app.services.user import (
    convert_password_to_hashed_one, verify_password_and_hashed_one
)
from app.services.constant import HashTestConst


class TestPasswordToHashedPassword():
    """
    パスワードをハッシュ化させるメソッドpassword_to_hashed_passwordについてのテスト
    """
    @pytest.mark.parametrize('password', HashTestConst.CORRECT_PASSWORD_LIST)
    def test_hashed_password_is_not_equal_password(self, password):
        """
        postエンドポイントに対して、適切なデータを送信すればユーザ登録ができることを確認。
        """
        hashed_password: str = convert_password_to_hashed_one(password)

        assert password != hashed_password


class TestVerifyPassword:
    """
    パスワード検証用メソッド
    """
    @pytest.mark.parametrize('password', HashTestConst.CORRECT_PASSWORD_LIST)
    def test_input_hashed_pass_and_raw_pass_should_return_true(self, password):
        """
        パスワードとハッシュ化パスワードを入力するとTrueを返却する
        """
        hashed_password: str = convert_password_to_hashed_one(password)
        assert verify_password_and_hashed_one(hashed_password, password)
