from django.urls import reverse
from django.http import HttpResponse
from urllib.parse import urlencode

from main.utils import GenericTestCase


class SearchTests(GenericTestCase):
    def setUp(self) -> None:
        self.setUpSessionAuth()

    def test_search(self) -> None:
        article = self.create_article(heading="find_me")

        r = self.search_article(article.heading)

        # count=3: 1st in the title tag, 2nd in the main page heading
        # (Search results by query: "find_me") and 3rd in the article card
        self.assertContains(r, article.heading, count=3)

    def test_search_by_author(self) -> None:
        article = self.create_article(heading="my new article")

        r = self.search_article(self.user.username)

        self.assertContains(r, self.article.heading)
        self.assertContains(r, article.heading)

    def test_search_by_part_of_article_heading(self) -> None:
        heading = "nicest article"
        self.create_article(heading=heading)

        query = heading[:5]
        r = self.search_article(query)

        self.assertContains(r, heading)

    # ========================
    # ====== Test utils ======
    # ========================
    def search_article(self, query: str) -> HttpResponse:
        """Searches for an article by `query` using GET."""
        url = reverse("search")
        r = self.client.post(
            url, urlencode({"search_query": query}),
            content_type="application/x-www-form-urlencoded", follow=True
        )

        return r
