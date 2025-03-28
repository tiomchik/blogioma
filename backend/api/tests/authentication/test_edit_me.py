from .generic import AuthenticationGenericTestCase


class EditMeTests(AuthenticationGenericTestCase):
    def test_change_username(self) -> None:
        data = {"username": "updated_test_user"}
        r = self.update_user_data(data)

        self.assertOkStatus(r)
        self.assertContains(r, data["username"])

    def test_change_password(self) -> None:
        previous_password = self.user.password
        data = {"password": "new_password"}
        r = self.update_user_data(data)

        self.user.refresh_from_db()
        self.assertOkStatus(r)
        self.assertNotEqual(previous_password, self.user.password)
