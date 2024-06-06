from django.urls import reverse
from urllib.parse import urlencode

from main.utils import GenericTestCase


class ProfileTests(GenericTestCase):
    def setUp(self) -> None:
        self.setUpSessionAuth()

    def test_set_social_links(self) -> None:
        data = {
            "youtube": "https://www.youtube.com/",
            "tiktok": "https://tiktok.com/",
            "twitch": "https://twitch.tv/",
            "linkedin": "https://linkedin.com/",
        }
        r = self._set_social_links(**data)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.profile.youtube, data["youtube"])
        self.assertEqual(self.profile.tiktok, data["tiktok"])
        self.assertEqual(self.profile.twitch, data["twitch"])
        self.assertEqual(self.profile.linkedin, data["linkedin"])

    def test_read_social_links(self) -> None:
        self._set_social_links()

        url = reverse("see_profile", kwargs={"username": self.user.username})
        r = self.client.get(url)

        self.assertIn(self.profile.youtube, str(r.content))
        self.assertIn(self.profile.tiktok, str(r.content))
        self.assertIn(self.profile.twitch, str(r.content))
        self.assertIn(self.profile.linkedin, str(r.content))

    def test_update_social_links(self) -> None:
        self._set_social_links()

        url = reverse(
            "social_media_links", kwargs={"username": self.user.username}
        )
        youtube = "https://www.youtube.com/@test"
        data = urlencode({"youtube": youtube})
        self.client.post(
            url, data, content_type="application/x-www-form-urlencoded",
            follow=True
        )

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.youtube, youtube)

    def test_delete_social_links(self) -> None:
        self._set_social_links()
        self._set_social_links(youtube="", tiktok="", twitch="", linkedin="")

        self.assertEqual(self.profile.youtube, "")
        self.assertEqual(self.profile.tiktok, "")
        self.assertEqual(self.profile.twitch, "")
        self.assertEqual(self.profile.linkedin, "")

    # ========================
    # ====== Test utils ======
    # ========================
    def _set_social_links(
        self, youtube: str = "https://www.youtube.com/",
        tiktok: str = "https://tiktok.com/",
        twitch: str = "https://twitch.tv/",
        linkedin: str = "https://linkedin.com/"
    ):
        """Sets a passed social media links to the `self.profile`
        using POST."""
        url = reverse(
            "social_media_links", kwargs={"username": self.user.username}
        )
        data = urlencode({
            "youtube": youtube, "tiktok": tiktok, "twitch": twitch,
            "linkedin": linkedin
        })
        r = self.client.post(
            url, data, content_type="application/x-www-form-urlencoded",
            follow=True
        )
        self.profile.refresh_from_db()

        return r
