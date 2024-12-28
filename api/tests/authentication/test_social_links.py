from .generic import AuthenticationGenericTestCase


class SocialLinksTests(AuthenticationGenericTestCase):
    social_links_data = {
        "youtube": "https://www.youtube.com/",
        "tiktok": "https://tiktok.com/",
        "twitch": "https://twitch.tv/",
        "linkedin": "https://linkedin.com/",
    }

    def setUp(self):
        super().setUp()
        self.set_and_refresh_social_links(self.social_links_data)

    def test_read_social_links(self) -> None:
        r = self.get_me()
        self.assertContainsList(r, self.social_links_data.values())

    def test_update_social_links(self) -> None:
        youtube = "https://www.youtube.com/@test"
        r = self.set_and_refresh_social_links({"youtube": youtube})
        self.assertContains(r, youtube)

    def test_delete_social_links(self) -> None:
        r = self.set_and_refresh_social_links({
            "youtube": "",
            "tiktok": "",
            "twitch": "",
            "linkedin": "",
        })
        self.assertNotContainsList(r, self.social_links_data.values())
