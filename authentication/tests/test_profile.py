from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode

from main.utils import GenericTestCase


class ProfileTests(GenericTestCase):
    def setUp(self) -> None:
        self.setUpSessionAuth()

    def test_get_profile(self) -> None:
        url = reverse(
            "see_profile", kwargs={"username": self.profile.user.username}
        )
        r = self.client.get(url)
        self.assertContains(r, self.profile.user.username)

    def test_get_profile_articles(self) -> None:
        article = self._create_article(headling="article")
        article1 = self._create_article(headling="article1")
        article2 = self._create_article(headling="article2")

        cache.clear()
        url = reverse(
            "see_profile", kwargs={"username": self.profile.user.username}
        )
        r = self.client.get(url)

        self.assertContains(r, article.headling)
        self.assertContains(r, article1.headling)
        self.assertContains(r, article2.headling)

    def test_change_pfp(self) -> None:
        with open("authentication/tests/cat.jpg", "rb") as pfp:
            new_pfp = SimpleUploadedFile(
                "cat.jpg", pfp.read(), content_type="image/jpeg"
            )

        url = reverse("change_pfp")
        self.client.post(
            url, {"new_pfp": new_pfp}, follow=True, format="multipart"
        )

        self.profile.refresh_from_db()
        self.assertIsNotNone(self.profile.pfp)

    def test_change_username(self) -> None:
        username = "new_username"
        data = urlencode({
            "new_username": username, "captcha_0": "value",
            "captcha_1": "PASSED"
        })
        url = reverse("change_username")
        self.client.post(
            url, data, follow=True,
            content_type="application/x-www-form-urlencoded"
        )

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.user.username, username)

    def test_change_password(self) -> None:
        password = "new_password"
        data = urlencode({
            "new_password": password, "new_password1": password,
            "captcha_0": "value", "captcha_1": "PASSED"
        })
        url = reverse("change_password")
        self.client.post(
            url, data, content_type="application/x-www-form-urlencoded"
        )

        previous_password = self.user.password
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.password, previous_password)

    # ==========================
    # ====== Social links ======
    # ==========================
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
        cache.clear()
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
    ) -> HttpResponse:
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
