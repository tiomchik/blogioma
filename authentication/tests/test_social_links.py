from .generic import AuthenticationGenericTestCase


class SocialLinksTests(AuthenticationGenericTestCase):
    social_links = {
        "youtube": "https://www.youtube.com/",
        "tiktok": "https://tiktok.com/",
        "twitch": "https://twitch.tv/",
        "linkedin": "https://linkedin.com/",
    }

    def setUp(self) -> None:
        self.setUpSessionAuth()
        self.set_and_refresh_social_links(self.social_links)

    def test_read_social_links(self) -> None:
        r = self.get_profile_page()
        for field in self.social_links.keys():
            self.assertContains(r, getattr(self.user, field))

    def test_update_social_links(self) -> None:
        youtube = "https://www.youtube.com/@test"
        self.set_and_refresh_social_links({"youtube": youtube})
        self.assertEqual(self.user.youtube, youtube)

    def test_delete_social_links(self) -> None:
        self.set_and_refresh_social_links({
            "youtube": "",
            "tiktok": "",
            "twitch": "",
            "linkedin": ""
        })
        for field in self.social_links.keys():
            self.assertEqual(getattr(self.user, field), "")
