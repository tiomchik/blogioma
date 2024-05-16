from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse

from articles.models import Article
from authentication.models import Profile
from feedback.models import Report


class ArticleTests(APITestCase):
    def setUp(self) -> None:
        data = {"username": "test_user1", "password": "12341234"}
        self._register_user(**data)

        self.user = User.objects.get(username=data["username"])
        self.profile = Profile.objects.get(user=self.user)
        self.token = self._obtain_token(**data)

    # ==================
    # ===== Create =====
    # ==================
    def test_create(self) -> None:
        url = reverse("article-list")
        data = {
            "headling": "lorem ipsum dolor",
            "full_text": "lorem ipsum dolor test"
        }
        r = self.client.post(
            url, data, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json().get("headling"), data["headling"])
        self.assertEqual(r.json().get("full_text"), data["full_text"])
        self.assertEqual(
            r.json().get("author").get("user").get("username"),
            self.user.username
        )

    def test_unauth_create(self) -> None:
        url = reverse("article-list")
        data = {
            "headling": "lorem ipsum dolor",
            "full_text": "lorem ipsum dolor test"
        }
        r = self.client.post(url, data)

        self._check_unauth_response(r)

    def test_create_without_headling(self) -> None:
        url = reverse("article-list")
        data = {"full_text": "lorem ipsum dolor test"}
        r = self.client.post(
            url, data, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("headling"), ["This field is required."]
        )

    def test_create_with_very_long_headling(self) -> None:
        url = reverse("article-list")
        data = {
            "headling": "lorem ipsum dolorrrrrrrrrrrrrrrrrrrrrrr",
            "full_text": "lorem ipsum dolor test"
        }
        r = self.client.post(
            url, data, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("headling"),
            ["Ensure this field has no more than 32 characters."]
        )

    def test_create_without_full_text(self) -> None:
        url = reverse("article-list")
        data = {"headling": "lorem ipsum dolor"}
        r = self.client.post(
            url, data, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("full_text"), ["This field is required."]
        )

    # ==================
    # ====== Read ======
    # ==================
    def test_read_article_list(self) -> None:
        data = {
            "headling": "test_article_list",
            "full_text": "lorem ipsum dolor",
            "author": self.profile
        }
        Article.objects.create(**data)

        url = reverse("article-list")
        r = self.client.get(url)

        self._response_contains_article(r, data)

    def test_read_article_detail(self) -> None:
        data = {
            "headling": "test_article_detail",
            "full_text": "lorem ipsum dolor",
            "author": self.profile
        }
        article = Article.objects.create(**data)

        url = reverse("article-detail", kwargs={"pk": article.pk})
        r = self.client.get(url)

        self._response_contains_article(r, data)

    def test_search(self) -> None:
        data = {
            "headling": "find_me",
            "full_text": "lorem ipsum dolor",
            "author": self.profile
        }
        Article.objects.create(**data)

        url = reverse("article-list") + f"?q={data.get('headling')}"
        r = self.client.get(url)

        self._response_contains_article(r, data)

    # ====================
    # ====== Update ======
    # ====================
    def test_update(self) -> None:
        article = self._create_article()

        update_data = {
            "headling": "test_article_update is passed",
            "full_text": "lorem_ipsum_dolor"
        }
        r = self._update_article(article.pk, update_data)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self._response_contains_article(r, update_data)

    def test_update_without_headling(self) -> None:
        article = self._create_article()

        update_data = {"full_text": "lorem_ipsum_dolor"}
        r = self._update_article(article.pk, update_data)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("headling"), ["This field is required."]
        )

    def test_update_with_very_long_headling(self) -> None:
        article = self._create_article()

        update_data = {
            "headling":
                "test_article_update is NOOOOOOOOOOOOOOOOOOOOOOOOOOOT passed",
            "full_text": "lorem_ipsum_dolor"
        }
        r = self._update_article(article.pk, update_data)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("headling"),
            ["Ensure this field has no more than 32 characters."]
        )

    def test_update_without_full_text(self) -> None:
        article = self._create_article()

        update_data = {"headling": "test_article_update is NOT passed"}
        r = self._update_article(article.pk, update_data)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            r.json().get("full_text"), ["This field is required."]
        )

    def test_unauth_update(self) -> None:
        article = self._create_article()

        update_data = {
            "headling": "test_article_update is NOT passed",
            "full_text": "lorem_ipsum_dolor"
        }
        r = self._update_article(article.pk, update_data, auth=False)

        self._check_unauth_response(r)

    def test_update_nonuser_article(self) -> None:
        article = self._create_article()

        # Creating another user
        another_user_data = {"username": "test_user2", "password": "43214321"}
        self._register_user(**another_user_data)
        another_user_token = self._obtain_token(**another_user_data)

        update_data = {
            "headling": "hahahah i updated your article",
            "full_text": "no lorem ipsum dolor"
        }
        r = self._update_article(
            article.pk, update_data, token=another_user_token
        )

        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            r.json().get("detail"),
            "You do not have permission to perform this action."
        )

    # ====================
    # ====== Delete ======
    # ====================
    def test_delete(self) -> None:
        article = self._create_article()

        url = reverse("article-detail", kwargs={"pk": article.pk})
        r = self.client.delete(
            url, headers={"Authorization": f"Token {self.token}"}
        )
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

        # Trying to get deleted article
        r = self.client.get(url)

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            r.json().get("detail"), "No Article matches the given query."
        )

    def test_delete_nonuser_article(self) -> None:
        article = self._create_article()

        another_user_data = {"username": "test_user3", "password": "43214321"}
        self._register_user(**another_user_data)
        another_user_token = self._obtain_token(**another_user_data)

        url = reverse("article-detail", kwargs={"pk": article.pk})
        r = self.client.delete(
            url, headers={"Authorization": f"Token {another_user_token}"}
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    # ====================
    # ====== Report ======
    # ====================
    def test_report(self) -> None:
        article = self._create_article()

        url = reverse("report-article", kwargs={"pk": article.pk})
        r = self.client.post(
            url, {"reason": "Scam"},
            headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        report = Report.objects.get(pk=r.json().get("id"))
        self.assertIsNotNone(article.reports.get(pk=report.pk))

    def test_unauth_report(self) -> None:
        article = self._create_article()

        url = reverse("report-article", kwargs={"pk": article.pk})
        r = self.client.post(url, {"reason": "Scam"})

        self._check_unauth_response(r)

    # ========================
    # ====== Test utils ======
    # ========================
    def _response_contains_article(
        self, r: HttpResponse, article_data: dict, html: bool = False
    ) -> None:
        """Checks that response contains headling and full text
        from `article_data`."""
        self.assertContains(r, article_data.get("headling"), html=html)
        self.assertContains(r, article_data.get("full_text"), html=html)
        self.assertContains(r, self.user.username, html=html)

    def _check_unauth_response(self, r: HttpResponse) -> None:
        """Checks that response is returned error of unauthorized user."""
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            r.json().get("detail"),
            "Authentication credentials were not provided."
        )

    def _create_article(self) -> Article:
        """Creates articleand returns it. Article's data:
        
        Headling: test_article
        Full text: lorem ipsum dolor
        Author: `self.profile` """
        data = {
            "headling": "test_article",
            "full_text": "lorem ipsum dolor",
            "author": self.profile
        }
        return Article.objects.create(**data)

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

    def _obtain_token(self, **user_data) -> str:
        """Obtains token according to passed `user_data`."""
        token_url = reverse("obtain-token")
        token: str = self.client.post(
            token_url, user_data
        ).json().get("token")

        return token

    def _register_user(self, **user_data) -> HttpResponse:
        """Registers a user with `user_data`."""
        url = reverse("register")
        return self.client.post(url, user_data)
