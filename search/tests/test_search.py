from .generic import SearchGenericTestCase


class SearchTests(SearchGenericTestCase):
    def test_search(self) -> None:
        r = self.search(self.article.heading)

        # count=3: 1st in the title tag, 2nd in the main page heading
        # (Search results by query: "find_me") and 3rd in the article card
        self.assertContains(r, self.article.heading, count=3)

    def test_search_by_author(self) -> None:
        r = self.search(self.user.username)
        self.assertContains(r, self.article.heading)

    def test_search_by_part_of_article_heading(self) -> None:
        query = self.article.heading[:5]
        r = self.search(query)
        self.assertContains(r, self.article.heading)
