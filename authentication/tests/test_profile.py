from .generic import AuthenticationGenericTestCase


class ProfileTests(AuthenticationGenericTestCase):
    def test_get_profile(self) -> None:
        r = self.get_profile_page()
        self.assertContains(r, self.user.username)

    def test_get_profile_articles(self) -> None:
        articles = self.create_list_of_articles(3)
        r = self.get_profile_page()
        self.assertResponseContainsArticles(r, articles)

    def test_change_pfp(self) -> None:
        new_pfp = self.load_pfp("authentication/tests/cat.jpg")
        self.change_pfp(new_pfp)
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.pfp)

    def test_change_username(self) -> None:
        username = "new_username"
        self.change_username(username)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, username)

    def test_change_password(self) -> None:
        password = "new_password"
        self.change_password(password)
        previous_password = self.user.password
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.password, previous_password)
