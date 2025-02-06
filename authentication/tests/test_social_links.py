from django.core.cache import cache
from django.urls import reverse

from .generic import AuthenticationGenericTestCase


class SocialLinksTests(AuthenticationGenericTestCase):
    social_links = {
        "youtube": "https://www.youtube.com/",
        "tiktok": "https://tiktok.com/",
        "twitch": "https://twitch.tv/",
        "linkedin": "https://linkedin.com/",
    }

    def test_set_social_links(self) -> None:
        r = self.set_and_refresh_social_links(self.social_links)
        self.assertOkStatus(r)
        for field in self.social_links.keys():
            self.assertEqual(
                getattr(self.user, field), self.social_links[field]
            )

    def test_read_social_links(self) -> None:
        self.set_and_refresh_social_links(self.social_links)

        url = reverse("see_profile", kwargs={"username": self.user.username})
        cache.clear()
        r = self.client.get(url)

        for field in self.social_links.keys():
            self.assertContains(r, getattr(self.user, field))

    def test_update_social_links(self) -> None:
        self.set_and_refresh_social_links(self.social_links)

        youtube = "https://www.youtube.com/@test"
        self.set_and_refresh_social_links({"youtube": youtube})

        self.assertEqual(self.user.youtube, youtube)

    def test_delete_social_links(self) -> None:
        self.set_and_refresh_social_links(self.social_links)
        self.set_and_refresh_social_links({
            "youtube": "",
            "tiktok": "",
            "twitch": "",
            "linkedin": ""
        })
        for field in self.social_links.keys():
            self.assertEqual(getattr(self.user, field), "")
