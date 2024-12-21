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
        r = self._set_social_links(self.social_links_data)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertContains(r, self.social_links_data["youtube"])
        self.assertContains(r, self.social_links_data["tiktok"])
        self.assertContains(r, self.social_links_data["twitch"])
        self.assertContains(r, self.social_links_data["linkedin"])

    def test_read_social_links(self) -> None:
        self._set_social_links(self.social_links_data)
        url = reverse("me")
        r = self.client.get(url, headers=self.authorization_header)

        self.assertContains(r, self.user.youtube)
        self.assertContains(r, self.user.tiktok)
        self.assertContains(r, self.user.twitch)
        self.assertContains(r, self.user.linkedin)

    def test_update_social_links(self) -> None:
        self._set_social_links(self.social_links_data)
        youtube = "https://www.youtube.com/@test"
        r = self._set_social_links({"youtube": youtube})
        self.assertContains(r, youtube)

    def test_delete_social_links(self) -> None:
        self._set_social_links(self.social_links_data)
        r = self._set_social_links({
            "youtube": "",
            "tiktok": "",
            "twitch": "",
            "linkedin": "",
        })

        self.assertEqual(r.json().get("youtube"), "")
        self.assertEqual(r.json().get("tiktok"), "")
        self.assertEqual(r.json().get("twitch"), "")
        self.assertEqual(r.json().get("linkedin"), "")
