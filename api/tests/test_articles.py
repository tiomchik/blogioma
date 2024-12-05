from rest_framework import status
from django.http import HttpResponse
from django.urls import reverse

from articles.models import Article
from feedback.models import Report
from main.utils import GenericTestCase


class ArticleTests(GenericTestCase):
    def test_create(self) -> None:
        url = reverse("article-list")
        data = {
            "heading": "lorem ipsum dolor",
            "full_text": "lorem ipsum dolor test"
        }
        r = self.client.post(
            url, data, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json().get("heading"), data["heading"])
        self.assertEqual(r.json().get("full_text"), data["full_text"])
        self.assertEqual(
            r.json().get("author").get("username"),
            self.user.username
        )

    def test_unauth_create(self) -> None:
        url = reverse("article-list")
        data = {
            "heading": "lorem ipsum dolor",
            "full_text": "lorem ipsum dolor test"
        }
        r = self.client.post(url, data)

        self._check_unauth_response(r)

    def test_create_without_heading(self) -> None:
        url = reverse("article-list")
        data = {"full_text": "lorem ipsum dolor test"}
        r = self.client.post(
            url, data, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("heading"), ["This field is required."]
        )

    def test_create_with_very_long_heading(self) -> None:
        url = reverse("article-list")
        data = {
            "heading": "lorem ipsum dolorrrrrrrrrrrrrrrrrrrrrrr" * 10,
            "full_text": "lorem ipsum dolor test"
        }
        r = self.client.post(
            url, data, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("heading"),
            ["Ensure this field has no more than 100 characters."]
        )

    def test_create_without_full_text(self) -> None:
        url = reverse("article-list")
        data = {"heading": "lorem ipsum dolor"}
        r = self.client.post(
            url, data, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("full_text"), ["This field is required."]
        )

    def test_read_list(self) -> None:
        data = {
            "heading": "test_article_list",
            "full_text": "lorem ipsum dolor",
            "author": self.user
        }
        Article.objects.create(**data)

        url = reverse("article-list")
        r = self.client.get(url)

        self._response_contains_article(r, data)

    def test_read_detail(self) -> None:
        data = {
            "heading": "test_article_detail",
            "full_text": "lorem ipsum dolor",
            "author": self.user
        }
        article = Article.objects.create(**data)

        url = reverse("article-detail", kwargs={"pk": article.pk})
        r = self.client.get(url)

        self._response_contains_article(r, data)

    def test_search(self) -> None:
        data = {
            "heading": "find_me",
            "full_text": "lorem ipsum dolor",
            "author": self.user
        }
        Article.objects.create(**data)

        url = reverse("article-list") + f"?q={data.get('heading')}"
        r = self.client.get(url)

        self._response_contains_article(r, data)

    def test_random(self) -> None:
        for i in range(10):
            self._create_article(heading=f"test_article{i}")

        url = reverse("article-random-article")
        r = self.client.get(url)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(r.json().get("heading"))
        self.assertIsNotNone(r.json().get("full_text"))
        self.assertIsNotNone(r.json().get("author"))

    def test_update(self) -> None:
        update_data = {
            "heading": "test_article_update is passed",
            "full_text": "lorem_ipsum_dolor"
        }
        r = self._update_article(self.article.pk, update_data)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self._response_contains_article(r, update_data)

    def test_update_without_heading(self) -> None:
        update_data = {"full_text": "lorem_ipsum_dolor"}
        r = self._update_article(self.article.pk, update_data)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("heading"), ["This field is required."]
        )

    def test_update_with_very_long_heading(self) -> None:
        update_data = {
            "heading":
                "test_article_update is NOOOOOOOOOOOOOOOOOOOOOOOT passed" * 2,
            "full_text": "lorem_ipsum_dolor"
        }
        r = self._update_article(self.article.pk, update_data)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("heading"),
            ["Ensure this field has no more than 100 characters."]
        )

    def test_update_without_full_text(self) -> None:
        update_data = {"heading": "test_article_update is NOT passed"}
        r = self._update_article(self.article.pk, update_data)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("full_text"), ["This field is required."]
        )

    def test_unauth_update(self) -> None:
        update_data = {
            "heading": "test_article_update is NOT passed",
            "full_text": "lorem_ipsum_dolor"
        }
        r = self._update_article(self.article.pk, update_data, auth=False)

        self._check_unauth_response(r)

    def test_update_nonuser_article(self) -> None:
        another_user_data = {
            "username": "test_user2",
            "password": "43214321",
            "email": "test2@test.com"
        }
        self._register_user(**another_user_data)
        another_user_token = self._obtain_token(**another_user_data)

        update_data = {
            "heading": "hahahah i updated your article",
            "full_text": "no lorem ipsum dolor"
        }
        r = self._update_article(
            self.article.pk, update_data, token=another_user_token
        )

        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            r.json().get("detail"),
            "You do not have permission to perform this action."
        )

    def test_delete(self) -> None:
        url = reverse("article-detail", kwargs={"pk": self.article.pk})
        r = self.client.delete(
            url, headers={"Authorization": f"Token {self.token}"}
        )
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

        r = self.client.get(url)

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            r.json().get("detail"), "No Article matches the given query."
        )

    def test_delete_nonuser_article(self) -> None:
        another_user_data = {
            "username": "test_user3",
            "password": "43214321",
            "email": "test3@test.com"
        }
        self._register_user(**another_user_data)
        another_user_token = self._obtain_token(**another_user_data)

        url = reverse("article-detail", kwargs={"pk": self.article.pk})
        r = self.client.delete(
            url, headers={"Authorization": f"Token {another_user_token}"}
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_report(self) -> None:
        url = reverse("report-article", kwargs={"pk": self.article.pk})
        r = self.client.post(
            url, {"reason": "Scam"},
            headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        report = Report.objects.get(pk=r.json().get("id"))
        self.assertIsNotNone(self.article.reports.get(pk=report.pk))

    def test_unauth_report(self) -> None:
        url = reverse("report-article", kwargs={"pk": self.article.pk})
        r = self.client.post(url, {"reason": "Scam"})

        self._check_unauth_response(r)

    def _response_contains_article(
        self, r: HttpResponse, article_data: dict, html: bool = False
    ) -> None:
        """Checks that response contains heading and full text
        from `article_data`."""
        self.assertContains(r, article_data.get("heading"), html=html)
        self.assertContains(r, article_data.get("full_text"), html=html)
        self.assertContains(r, self.user.username, html=html)

    def _update_article(
        self, pk: int, data: dict, auth: bool = True, token: str = None
    ) -> HttpResponse:
        """Updates article according to passed `data`."""
        headers = {}
        if auth:
            headers["Authorization"] = (
                f"Token {token if token else self.token}"
            )

        url = reverse("article-detail", kwargs={"pk": pk})
        r = self.client.put(url, data, headers=headers)

        return r
