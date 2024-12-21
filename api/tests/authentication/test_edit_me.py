from django.urls import reverse
from rest_framework import status

from .generic import AuthenticationGenericTestCase


class EditMeTests(AuthenticationGenericTestCase):
    url = reverse("edit-me")

    def test_change_username(self) -> None:
        data = {"username": "updated_test_user"}
        r = self.client.put(self.url, data, headers=self.auth_header)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertContains(r, data["username"])

    def test_change_password(self) -> None:
        previous_password = self.user.password
        data = {"password": "new_password"}
        r = self.client.put(self.url, data, headers=self.auth_header)

        self.user.refresh_from_db()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertNotEqual(previous_password, self.user.password)
