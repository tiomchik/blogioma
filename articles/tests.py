from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode

from feedback.models import Report
from main.utils import GenericTestCase
from .models import Article


class ArticleTests(GenericTestCase):
    def setUp(self) -> None:
        self.setUpSessionAuth()

    # ====================
    # ====== Create ======
    # ====================
    def test_create(self) -> None:
        headling = "article test"
        full_text = "lorem ipsum dolor"
        data = urlencode({"headling": headling, "full_text": full_text})
        self._post_article(data)

        self.assertTrue(Article.objects.filter(headling=headling).exists())

    def test_unauth_create(self) -> None:
        self.client.logout()

        headling = "article test"
        full_text = "lorem ipsum dolor"
        data = urlencode({"headling": headling, "full_text": full_text})
        self._post_article(data)

        self.assertFalse(Article.objects.filter(headling=headling).exists())

    def test_create_without_headling(self) -> None:
        full_text = "lorem ipsum dolor without headling"
        data = urlencode({"full_text": full_text})
        self._post_article(data)

        self.assertFalse(Article.objects.filter(full_text=full_text).exists())

    def test_create_with_very_long_headling(self) -> None:
        headling = "article test" * 10
        full_text = "lorem ipsum dolor"
        data = urlencode({"headling": headling, "full_text": full_text})
        self._post_article(data)

        self.assertFalse(Article.objects.filter(headling=headling).exists())

    def test_create_without_full_text(self) -> None:
        headling = "article test"
        data = urlencode({"headling": headling})
        self._post_article(data)

        self.assertFalse(Article.objects.filter(headling=headling).exists())

    # ==================
    # ====== Read ======
    # ==================
    def test_read_at_home_page(self) -> None:
        url = reverse("home")
        r = self.client.get(url)

        self.assertContains(r, self.article.headling)

    def test_read_detail(self) -> None:
        url = reverse("read", kwargs={"pk": self.article.pk})
        r = self.client.get(url)

        self.assertContains(r, self.article.headling)
        self.assertContains(r, self.article.full_text)
        self.assertContains(r, self.article.author.user.username)

    def test_random(self) -> None:
        url = reverse("random_article")
        r = self.client.get(url, follow=True)

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, self.article.full_text)

    # ====================
    # ====== Update ======
    # ====================
    def test_update(self) -> None:
        headling = "updated article"
        full_text = "new lorem ipsum dolor"
        data = urlencode({"headling": headling, "full_text": full_text})
        self._update_article(data)

        self.assertTrue(Article.objects.filter(headling=headling).exists())

    def test_update_without_headling(self) -> None:
        full_text = "new lorem ipsum dolor"
        data = urlencode({"full_text": full_text})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(full_text=full_text).exists())

    def test_update_with_very_long_headling(self) -> None:
        headling = "updated article" * 10
        full_text = "new lorem ipsum dolor"
        data = urlencode({"headling": headling, "full_text": full_text})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(headling=headling).exists())

    def test_update_without_full_text(self) -> None:
        headling = "updated article"
        data = urlencode({"headling": headling})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(headling=headling).exists())

    def test_unauth_update(self) -> None:
        self.client.logout()

        headling = "updated article"
        full_text = "new lorem ipsum dolor"
        data = urlencode({"headling": headling, "full_text": full_text})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(headling=headling).exists())

    def test_update_nonuser_article(self) -> None:
        self._auth_to_another_user()

        headling = "updated article"
        full_text = "new lorem ipsum dolor"
        data = urlencode({"headling": headling, "full_text": full_text})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(headling=headling).exists())

    # ====================
    # ====== Delete ======
    # ====================
    def test_delete(self) -> None:
        r = self._del_article()
        self.assertEqual(r.status_code, 200)
        self.assertFalse(
            Article.objects.filter(headling=self.article.headling).exists()
        )

    def test_delete_nonuser_article(self) -> None:
        self._auth_to_another_user()

        r = self._del_article()
        self.assertTrue(
            Article.objects.filter(headling=self.article.headling).exists()
        )

    # ========================
    # ====== Test utils ======
    # ========================
    def _post_article(self, encoded_data: str) -> HttpResponse:
        """Creates an article using POST."""
        url = reverse("add_article")
        r = self.client.post(
            url, encoded_data,
            content_type="application/x-www-form-urlencoded", follow=True
        )

        return r

    def _update_article(self, encoded_data: str) -> HttpResponse:
        """Updates an article using POST."""
        url = reverse("update", kwargs={"pk": self.article.pk})
        r = self.client.post(
            url, encoded_data,
            content_type="application/x-www-form-urlencoded", follow=True
        )

        return r

    def _del_article(self) -> HttpResponse:
        """Deletes an article using GET."""
        url = reverse("delete", kwargs={"pk": self.article.pk})
        r = self.client.get(url, follow=True)

        return r
