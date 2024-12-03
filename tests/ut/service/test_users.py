# サードバーティ製モジュール
import pytest
from pytest_mock import MockFixture
from argon2.exceptions import VerifyMismatchError, InvalidHashError
# プロジェクトモジュール
from app.services.users import (
    convert_password_to_hashed_one, verify_password_and_hashed_one
)
from tests.ut.service.constant import HashTestConst


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

    @pytest.mark.parametrize('password', HashTestConst.CORRECT_PASSWORD_LIST)
    def test_input_hashed_pass_and_incorrect_pass_should_return_false(self, password):
        """
        間違ったパスワードとハッシュ化パスワードを入力するとVerifyMismatchErrorが発生する
        """
        hashed_password: str = convert_password_to_hashed_one(password)
        incorrect_password: str = str(password) + '1'

        assert (not verify_password_and_hashed_one(hashed_password, incorrect_password))

    @pytest.mark.parametrize('password', HashTestConst.CORRECT_PASSWORD_LIST)
    def test_input_invalid_hashed_pass_and_pass_should_return_false(self, password):
        """
        間違ったパスワードとハッシュ化パスワードを入力するとVerifyMismatchErrorが発生する
        """
        hashed_password: str = convert_password_to_hashed_one(password) + '1'
        assert (not verify_password_and_hashed_one(hashed_password, password))

    @pytest.mark.parametrize('password', HashTestConst.CORRECT_PASSWORD_LIST)
    def test_if_raise_mismatch_error_method_should_return_false(
            self, password, mocker: MockFixture):
        """
        VerifyMismatchErrorが発生した場合、falseが返却される。
        """
        mocker.patch( 'argon2.PasswordHasher.verify', side_effect=VerifyMismatchError() )
        hashed_password: str = convert_password_to_hashed_one(password)
        is_false: bool = verify_password_and_hashed_one(hashed_password, password) == False
        assert is_false

    @pytest.mark.parametrize('password', HashTestConst.CORRECT_PASSWORD_LIST)
    def test_if_raise_invalid_hash_error_method_should_return_false(
            self, password, mocker: MockFixture):
        """
        InvalidHashErrorが発生した場合、falseが返却される。
        """
        mocker.patch( 'argon2.PasswordHasher.verify', side_effect=InvalidHashError() )
        hashed_password: str = convert_password_to_hashed_one(password)
        is_false: bool = verify_password_and_hashed_one(hashed_password, password) == False
        assert is_false

    @pytest.mark.parametrize('password', HashTestConst.CORRECT_PASSWORD_LIST)
    def test_if_raise_exception_in_method_then_should_raise_exception(
            self, password, mocker: MockFixture):
        """
        VerifyMismatchError, InvalidHashError以外のエラーが発生した場合エラーが発生する。
        """
        mocker.patch( 'argon2.PasswordHasher.verify', side_effect=Exception() )
        hashed_password: str = convert_password_to_hashed_one(password)
        with pytest.raises(Exception):
            _ = verify_password_and_hashed_one(hashed_password, password)
