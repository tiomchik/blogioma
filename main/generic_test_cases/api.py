from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status

from authentication.models import User
from .generic_test_case import GenericTestCase


class APIGenericTestCase(GenericTestCase):
    def setUp(self) -> None:
        data = {"username": "test_user1", "password": "12341234"}
        self.register_user(**data)

        self.user = User.objects.get(username=data["username"])
        self.token = self._obtain_token(**data)
        self.auth_header = {"Authorization": f"Token {self.token}"}

    def _obtain_token(self, **user_data) -> str:
        token_url = reverse("obtain-token")
        token: str = self.client.post(
            token_url, user_data
        ).json().get("token")

        return token

    def _set_another_user(self, **another_user_data) -> None:
        self.register_user(**another_user_data)
        another_user_token = self._obtain_token(**another_user_data)
        self.auth_header = {
            "Authorization": f"Token {another_user_token}"
        }

    def assertUnauthResponse(self, r: HttpResponse) -> None:
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            r.json().get("detail"),
            "Authentication credentials were not provided."
        )

    def assertFieldIsRequiredInJson(self, r: HttpResponse, field: str) -> None:
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get(field), ["This field is required."]
        )

    def assertFieldIsTooLong(self, r: HttpResponse, field: str) -> None:
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        error: str = r.json().get(field)[0]
        self.assertTrue(error.startswith("Ensure this field has no more"))
        self.assertTrue(error.endswith(" characters."))

    def assertForbiddenResponse(self, r: HttpResponse) -> None:
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            r.json().get("detail"),
            "You do not have permission to perform this action."
        )

    def assertContainsList(self, r: HttpResponse, list: list) -> None:
        for item in list:
            self.assertContains(r, item)

    def assertNotContainsList(self, r: HttpResponse, list: list) -> None:
        for item in list:
            self.assertNotContains(r, item)

    def assertOkStatus(self, r: HttpResponse) -> None:
        self.assertEqual(r.status_code, status.HTTP_200_OK)
