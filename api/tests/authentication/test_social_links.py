from django.urls import reverse
from rest_framework import status

from .generic import AuthenticationGenericTestCase


class SocialLinksTests(AuthenticationGenericTestCase):
    url = reverse("me")
    social_links_data = {
        "youtube": "https://www.youtube.com/",
        "tiktok": "https://tiktok.com/",
        "twitch": "https://twitch.tv/",
        "linkedin": "https://linkedin.com/",
    }

    def test_set_social_links(self) -> None:
        r = self.set_and_refresh_social_links(self.social_links_data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        for link in self.social_links_data.values():
            self.assertContains(r, link)

    def test_read_social_links(self) -> None:
        self.set_and_refresh_social_links(self.social_links_data)
        r = self.client.get(self.url, headers=self.auth_header)
        for link in self.social_links_data.values():
            self.assertContains(r, link)

    def test_update_social_links(self) -> None:
        self.set_and_refresh_social_links(self.social_links_data)
        youtube = "https://www.youtube.com/@test"
        r = self.set_and_refresh_social_links({"youtube": youtube})
        self.assertContains(r, youtube)

    def test_delete_social_links(self) -> None:
        self.set_and_refresh_social_links(self.social_links_data)
        r = self.set_and_refresh_social_links({
            "youtube": "",
            "tiktok": "",
            "twitch": "",
            "linkedin": "",
        })

        for link in self.social_links_data.values():
            self.assertNotContains(r, link)
