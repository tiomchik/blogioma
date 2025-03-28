from authentication.models import User
from .generic import AuthenticationGenericTestCase


class SignUpTests(AuthenticationGenericTestCase):
    form_data = {
        "username": "test_user123",
        "password": "12341234",
        "password1": "12341234",
        "email": "test@test.com",
        "captcha_0": "value",
        "captcha_1": "PASSED",
    }

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_sign_up(self) -> None:
        self.sign_up_user(self.form_data)
        created_user = User.objects.filter(
            username=self.form_data["username"]
        )
        self.assertTrue(created_user.exists())

    def test_sign_up_without_username(self) -> None:
        self.form_data.pop("username")
        r = self.sign_up_user(self.form_data)
        self.assertFieldIsRequiredOnPage(r)

    def test_sign_up_without_password(self) -> None:
        self.form_data.pop("password")
        r = self.sign_up_user(self.form_data)
        self.assertFieldIsRequiredOnPage(r)

    def test_sign_up_with_invalid_email(self) -> None:
        self.form_data["email"] = "invalid_email"
        r = self.sign_up_user(self.form_data)
        self.assertContains(r, "Enter a valid email address")

    def test_sign_up_with_non_unique_email(self) -> None:
        email = "test@test.com"
        self.register_user(
            username="new_user", email=email, password="12341234"
        )
        self.form_data["email"] = email
        r = self.sign_up_user(self.form_data)
        self.assertContains(r, "This email already busy")
