from django.urls import reverse
from main.generic_test_cases.api import APIGenericTestCase


class ReadUserTests(APIGenericTestCase):
    def test_read_detail(self) -> None:
        url = reverse("user-detail", kwargs={"pk": self.user.pk})
        r = self.client.get(url)
        self.assertEqual(r.json().get("id"), self.user.id)
        self.assertEqual(r.json().get("username"), self.user.username)
        self.assertEqual(r.json().get("email"), self.user.email)
