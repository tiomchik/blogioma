from django.core.cache import cache
from django.urls import reverse
from urllib.parse import urlencode

from .generic import AuthenticationGenericTestCase


class SocialLinksTests(AuthenticationGenericTestCase):
    def test_set_social_links(self) -> None:
        data = {
            "youtube": "https://www.youtube.com/",
            "tiktok": "https://tiktok.com/",
            "twitch": "https://twitch.tv/",
            "linkedin": "https://linkedin.com/",
        }
        r = self.set_social_links(**data)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.user.youtube, data["youtube"])
        self.assertEqual(self.user.tiktok, data["tiktok"])
        self.assertEqual(self.user.twitch, data["twitch"])
        self.assertEqual(self.user.linkedin, data["linkedin"])

    def test_read_social_links(self) -> None:
        self.set_social_links()

        url = reverse("see_profile", kwargs={"username": self.user.username})
        cache.clear()
        r = self.client.get(url)

        self.assertIn(self.user.youtube, str(r.content))
        self.assertIn(self.user.tiktok, str(r.content))
        self.assertIn(self.user.twitch, str(r.content))
        self.assertIn(self.user.linkedin, str(r.content))

    def test_update_social_links(self) -> None:
        self.set_social_links()

        url = reverse(
            "social_media_links", kwargs={"username": self.user.username}
        )
        youtube = "https://www.youtube.com/@test"
        data = urlencode({"youtube": youtube})
        self.client.post(
            url, data, content_type="application/x-www-form-urlencoded",
            follow=True
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.youtube, youtube)

    def test_delete_social_links(self) -> None:
        self.set_social_links()
        self.set_social_links(youtube="", tiktok="", twitch="", linkedin="")

        self.assertEqual(self.user.youtube, "")
        self.assertEqual(self.user.tiktok, "")
        self.assertEqual(self.user.twitch, "")
        self.assertEqual(self.user.linkedin, "")
