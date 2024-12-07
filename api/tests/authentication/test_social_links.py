from django.urls import reverse
from rest_framework import status

from .generic import AuthenticationGenericTestCase


class SocialLinksTests(AuthenticationGenericTestCase):
    url = reverse("me")

    def test_set_social_links(self) -> None:
        data = {
            "youtube": "https://www.youtube.com/",
            "tiktok": "https://tiktok.com/",
            "twitch": "https://twitch.tv/",
            "linkedin": "https://linkedin.com/",
        }
        r = self._set_social_links(**data)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertContains(r, data["youtube"])
        self.assertContains(r, data["tiktok"])
        self.assertContains(r, data["twitch"])
        self.assertContains(r, data["linkedin"])

    def test_read_social_links(self) -> None:
        self._set_social_links()
        url = reverse("me")
        r = self.client.get(
            url, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertContains(r, self.user.youtube)
        self.assertContains(r, self.user.tiktok)
        self.assertContains(r, self.user.twitch)
        self.assertContains(r, self.user.linkedin)

    def test_update_social_links(self) -> None:
        self._set_social_links()
        youtube = "https://www.youtube.com/@test"
        r = self._set_social_links(youtube=youtube)
        self.assertContains(r, youtube)

    def test_delete_social_links(self) -> None:
        self._set_social_links()
        r = self._set_social_links(
            youtube="", tiktok="", twitch="", linkedin=""
        )

        self.assertEqual(r.json().get("youtube"), "")
        self.assertEqual(r.json().get("tiktok"), "")
        self.assertEqual(r.json().get("twitch"), "")
        self.assertEqual(r.json().get("linkedin"), "")
