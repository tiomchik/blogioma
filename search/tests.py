from django.urls import reverse
from django.http import HttpResponse
from urllib.parse import urlencode

from main.utils import GenericTestCase


class SearchTests(GenericTestCase):
    def setUp(self) -> None:
        self.setUpSessionAuth()

    def test_search(self) -> None:
        article = self._create_article(headling="find_me")

        r = self._search_article(article.headling)

        # count=3: 1st in the title tag, 2nd in the main page headling
        # (Search results by query: "find_me") and 3rd in the article card
        self.assertContains(r, article.headling, count=3)

    def test_search_by_author(self) -> None:
        article = self._create_article(headling="my new article")

        r = self._search_article(self.user.username)

        self.assertContains(r, self.article.headling)
        self.assertContains(r, article.headling)

    def test_search_by_part_of_article_headling(self) -> None:
        headling = "nicest article"
        self._create_article(headling=headling)

        query = headling[:5]
        r = self._search_article(query)

        self.assertContains(r, headling)

    # ========================
    # ====== Test utils ======
    # ========================
    def _search_article(self, query: str) -> HttpResponse:
        """Searches for an article by `query` using GET."""
        url = reverse("search")
        r = self.client.post(
            url, urlencode({"search_query": query}),
            content_type="application/x-www-form-urlencoded", follow=True
        )

        return r
