from rest_framework import status

from .generic import CommentsGenericTestCase


class DeleteCommentTests(CommentsGenericTestCase):
    def test_delete(self) -> None:
        r = self._del_comment()
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauth_delete(self) -> None:
        r = self._del_comment(auth=False)
        self._check_unauth_response(r)

    def test_delete_nonuser_comment(self) -> None:
        another_user_data = {
            "username": "test_user3",
            "password": "12341234",
            "email": "test3@test.com"
        }
        self._register_user(**another_user_data)
        token = self._obtain_token(**another_user_data)

        r = self._del_comment(token=token)

        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            r.json().get("detail"),
            "You do not have permission to perform this action."
        )
