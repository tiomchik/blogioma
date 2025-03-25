from authentication.models import User
from .generic import GenericTestCase


class SessionAuthGenericTestCase(GenericTestCase):
    def setUp(self) -> None:
        user_data = {"username": "test_user", "password": "12341234"}
        self.user = User.objects.create_user(**user_data)
        self.client.login(**user_data)

    def auth_to_another_user(
        self, username: str = "test_user123", password: str = "12341234"
    ) -> None:
        self.client.logout()
        new_user_data = {"username": username, "password": password}
        User.objects.create(**new_user_data)
        self.client.login(**new_user_data)
