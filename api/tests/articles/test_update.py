from rest_framework import status

from .generic import ArticleGenericTestCase


class UpdateArticleTests(ArticleGenericTestCase):
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
