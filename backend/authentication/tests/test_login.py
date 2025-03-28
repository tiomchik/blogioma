from .generic import AuthenticationGenericTestCase


class LoginTests(AuthenticationGenericTestCase):
    form_data = {
        "username": "test_user123",
        "password": "12341234",
        "captcha_0": "value",
        "captcha_1": "PASSED",
    }

    def setUp(self) -> None:
        super().setUp()
        self.register_user(**self.form_data)
        self.client.logout()

    def test_login(self) -> None:
        r = self.login_user(self.form_data)
        self.assertUserIsAuthenticated(r)

    def test_login_without_username(self) -> None:
        self.form_data.pop("username")
        r = self.login_user(self.form_data)
        self.assertUserIsNotAuthenticated(r)

    def test_login_without_password(self) -> None:
        self.form_data.pop("password")
        r = self.login_user(self.form_data)
        self.assertUserIsNotAuthenticated(r)

    def test_login_with_invalid_username(self) -> None:
        self.form_data["username"] = "invalid_username"
        r = self.login_user(self.form_data)
        self.assertUserIsNotAuthenticated(r)

    def test_login_with_invalid_password(self) -> None:
        self.form_data["password"] = "invalid_password"
        r = self.login_user(self.form_data)
        self.assertUserIsNotAuthenticated(r)
