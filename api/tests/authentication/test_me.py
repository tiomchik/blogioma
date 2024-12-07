from django.urls import reverse
from rest_framework import status

from .generic import AuthenticationGenericTestCase


class MeTests(AuthenticationGenericTestCase):
    def test_me(self) -> None:
        url = reverse("me")
        r = self.client.get(url, headers={"Authorization": f"Token {self.token}"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("username"), self.user.username)

    def test_me_without_auth(self) -> None:
        url = reverse("me")
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
