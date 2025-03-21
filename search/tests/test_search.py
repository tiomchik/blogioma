from .generic import SearchGenericTestCase


class SearchTests(SearchGenericTestCase):
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
