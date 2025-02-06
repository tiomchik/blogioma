from django.core.cache import cache
from django.urls import reverse
from urllib.parse import urlencode

from .generic import AuthenticationGenericTestCase


class SocialLinksTests(AuthenticationGenericTestCase):
    form_data = {
        "youtube": "https://www.youtube.com/",
        "tiktok": "https://tiktok.com/",
        "twitch": "https://twitch.tv/",
        "linkedin": "https://linkedin.com/",
    }

    def test_set_social_links(self) -> None:
        r = self.set_and_refresh_social_links(self.form_data)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.user.youtube, self.form_data["youtube"])
        self.assertEqual(self.user.tiktok, self.form_data["tiktok"])
        self.assertEqual(self.user.twitch, self.form_data["twitch"])
        self.assertEqual(self.user.linkedin, self.form_data["linkedin"])

    def test_read_social_links(self) -> None:
        self.set_and_refresh_social_links(self.form_data)

        url = reverse("see_profile", kwargs={"username": self.user.username})
        cache.clear()
        r = self.client.get(url)

        self.assertIn(self.user.youtube, str(r.content))
        self.assertIn(self.user.tiktok, str(r.content))
        self.assertIn(self.user.twitch, str(r.content))
        self.assertIn(self.user.linkedin, str(r.content))

    def test_update_social_links(self) -> None:
        self.set_and_refresh_social_links(self.form_data)

        youtube = "https://www.youtube.com/@test"
        self.set_and_refresh_social_links({"youtube": youtube})

        self.assertEqual(self.user.youtube, youtube)

    def test_delete_social_links(self) -> None:
        self.set_and_refresh_social_links(self.form_data)
        self.set_and_refresh_social_links({
            "youtube": "",
            "tiktok": "",
            "twitch": "",
            "linkedin": ""
        })

        self.assertEqual(self.user.youtube, "")
        self.assertEqual(self.user.tiktok, "")
        self.assertEqual(self.user.twitch, "")
        self.assertEqual(self.user.linkedin, "")
