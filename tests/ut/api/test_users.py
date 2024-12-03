from fastapi.testclient import TestClient
from app.main import app

# テストクライアントの作成
client = TestClient(app)


class TestRegisterAccount:
    """
    アカウント登録に関するテスト
    """
    def test_valid_data_should_register_user_in_post():
        """
        postエンドポイントに対して、適切なデータを送信すればユーザ登録ができることを確認。
        """
        pass


    def test_invalid_data_should_register_user_in_post():
        """
        不適切なデータを送信した場合、ユーザ登録ができないことを確認。
        """
        pass


class TestLogin:
    """
    ログインに関するテスト
    """
    def test_user_can_login_with_valid_data():
        """
        適切なユーザ名とパスワードを入力すればログインできることを確認。
        """
        pass

    def test_user_can_not_login_with_invalid_data():
        """
        不適切なユーザ名とパスワードを入力してもログインできないことを確認。
        """
        pass


class TestModifyAccount:

    def test_root_can_delete_user():
        """
        管理者アカウントはユーザを削除することができることを確認。
        """
        pass


    def test_normal_user_can_nont_delete_user():
        """
        一般ユーザは自分以外のユーザ削除ができないことを確認。
        """
        pass


    def test_user_can_modify_own_account():
        """
        ユーザは自身のアカウントのデータを修正できることを確認。
        """
        pass


    def test_user_can_not_modify_another_account():
        """
        ユーザは他人のアカウントのデータを修正できないことを確認。
        """
        pass


class TestFetchUser:
    """
    ユーザ情報取得に関してのテスト
    """
    def test_should_fetch_all_users():
        """
        usersエンドポイントにアクセスすれば全ユーザを取得することができることを確認。
        """
        pass
