from .generic import AuthenticationGenericTestCase


class MeTests(AuthenticationGenericTestCase):
    def test_me(self) -> None:
        r = self.get_me()
        self.assertOkStatus(r)
        self.assertEqual(r.json().get("username"), self.user.username)

    def test_me_without_auth(self) -> None:
        self.auth_header = {}
        r = self.get_me()
        self.assertUnauthResponse(r)
