from django.http import HttpResponse
from django.urls import reverse
from main.generic_test_cases.api import APIGenericTestCase


class TestGetUserArticles(APIGenericTestCase):
    def test_get_user_articles(self) -> None:
        article = self.create_article()
        r = self.get_user_articles(self.user.username)
        self.assertContains(r, article.heading)

    def test_user_not_found(self) -> None:
        r = self.get_user_articles("non_existent_user")
        self.assertEqual(r.json().get("detail"), "User not found.")
        self.assertEqual(r.status_code, 404)

    def test_empty_list_of_articles(self) -> None:
        r = self.get_user_articles(self.user.username)
        self.assertEqual(r.json().get("results"), [])

    def get_user_articles(self, username: str) -> HttpResponse:
        url = reverse("user-articles", kwargs={"username": username})
        r = self.client.get(url)
        return r
