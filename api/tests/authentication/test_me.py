from rest_framework import status

from .generic import AuthenticationGenericTestCase


class MeTests(AuthenticationGenericTestCase):
    def test_me(self) -> None:
        r = self.get_me()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("username"), self.user.username)

    def test_me_without_auth(self) -> None:
        self.auth_header = {}
        r = self.get_me()
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
