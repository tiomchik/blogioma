from django.http import HttpResponse
from django.urls import reverse
from main.generic_test_cases.api import APIGenericTestCase


class ReadUserTests(APIGenericTestCase):
    def test_read_detail(self) -> None:
        r = self.get_user_detail(self.user.username)
        json_data = r.json()
        self.assertEqual(json_data.get("id"), self.user.id)
        self.assertEqual(json_data.get("username"), self.user.username)
        self.assertEqual(json_data.get("email"), self.user.email)

    def test_read_non_existent_user(self) -> None:
        r = self.get_user_detail("non_existent_user")
        self.assertEqual(r.status_code, 404)

    def get_user_detail(self, username: str) -> HttpResponse:
        url = reverse("user-detail", kwargs={"username": username})
        r = self.client.get(url)
        return r
