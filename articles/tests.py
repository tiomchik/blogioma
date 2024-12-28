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
        heading = "article test"
        full_text = "lorem ipsum dolor"
        data = urlencode({"heading": heading, "full_text": full_text})
        self._post_article(data)

        self.assertTrue(Article.objects.filter(heading=heading).exists())

    def test_unauth_create(self) -> None:
        self.client.logout()

        heading = "article test"
        full_text = "lorem ipsum dolor"
        data = urlencode({"heading": heading, "full_text": full_text})
        self._post_article(data)

        self.assertFalse(Article.objects.filter(heading=heading).exists())

    def test_create_without_heading(self) -> None:
        full_text = "lorem ipsum dolor without heading"
        data = urlencode({"full_text": full_text})
        self._post_article(data)

        self.assertFalse(Article.objects.filter(full_text=full_text).exists())

    def test_create_with_very_long_heading(self) -> None:
        heading = "article test" * 10
        full_text = "lorem ipsum dolor"
        data = urlencode({"heading": heading, "full_text": full_text})
        self._post_article(data)

        self.assertFalse(Article.objects.filter(heading=heading).exists())

    def test_create_without_full_text(self) -> None:
        heading = "article test"
        data = urlencode({"heading": heading})
        self._post_article(data)

        self.assertFalse(Article.objects.filter(heading=heading).exists())

    # ==================
    # ====== Read ======
    # ==================
    def test_read_at_home_page(self) -> None:
        url = reverse("home")
        r = self.client.get(url)

        self.assertContains(r, self.article.heading)

    def test_read_detail(self) -> None:
        url = reverse("read", kwargs={"pk": self.article.pk})
        r = self.client.get(url)

        self.assertContains(r, self.article.heading)
        self.assertContains(r, self.article.full_text)
        self.assertContains(r, self.article.author.username)

    def test_random(self) -> None:
        url = reverse("random_article")
        r = self.client.get(url, follow=True)

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, self.article.full_text)

    # ====================
    # ====== Update ======
    # ====================
    def test_update(self) -> None:
        heading = "updated article"
        full_text = "new lorem ipsum dolor"
        data = urlencode({"heading": heading, "full_text": full_text})
        self._update_article(data)

        self.assertTrue(Article.objects.filter(heading=heading).exists())

    def test_update_without_heading(self) -> None:
        full_text = "new lorem ipsum dolor"
        data = urlencode({"full_text": full_text})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(full_text=full_text).exists())

    def test_update_with_very_long_heading(self) -> None:
        heading = "updated article" * 10
        full_text = "new lorem ipsum dolor"
        data = urlencode({"heading": heading, "full_text": full_text})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(heading=heading).exists())

    def test_update_without_full_text(self) -> None:
        heading = "updated article"
        data = urlencode({"heading": heading})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(heading=heading).exists())

    def test_unauth_update(self) -> None:
        self.client.logout()

        heading = "updated article"
        full_text = "new lorem ipsum dolor"
        data = urlencode({"heading": heading, "full_text": full_text})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(heading=heading).exists())

    def test_update_nonuser_article(self) -> None:
        self.auth_to_another_user()

        heading = "updated article"
        full_text = "new lorem ipsum dolor"
        data = urlencode({"heading": heading, "full_text": full_text})
        self._update_article(data)

        self.assertFalse(Article.objects.filter(heading=heading).exists())

    # ====================
    # ====== Delete ======
    # ====================
    def test_delete(self) -> None:
        r = self._del_article()
        self.assertEqual(r.status_code, 200)
        self.assertFalse(
            Article.objects.filter(heading=self.article.heading).exists()
        )

    def test_delete_nonuser_article(self) -> None:
        self.auth_to_another_user()

        r = self._del_article()
        self.assertTrue(
            Article.objects.filter(heading=self.article.heading).exists()
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
