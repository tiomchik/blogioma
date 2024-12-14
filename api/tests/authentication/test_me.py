from django.urls import reverse
from rest_framework import status

from .generic import AuthenticationGenericTestCase


class MeTests(AuthenticationGenericTestCase):
    url = reverse("me")

    def test_me(self) -> None:
        r = self.client.get(self.url, headers=self.authorization_header)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("username"), self.user.username)

    def test_me_without_auth(self) -> None:
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
