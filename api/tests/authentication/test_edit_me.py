from django.urls import reverse
from rest_framework import status

from .generic import AuthenticationGenericTestCase


class EditMeTests(AuthenticationGenericTestCase):
    def test_change_username(self) -> None:
        data = {"username": "updated_test_user"}
        url = reverse("edit-me")
        r = self.client.put(
            url, data, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertContains(r, data["username"])

    def test_change_password(self) -> None:
        previous_password = self.user.password
        data = {"password": "new_password"}
        url = reverse("edit-me")
        r = self.client.put(
            url, data, headers={"Authorization": f"Token {self.token}"}
        )

        self.user.refresh_from_db()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertNotEqual(previous_password, self.user.password)
