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
            "see_profile", kwargs={"username": self.user.username}
        )
        r = self.client.get(url)
        self.assertContains(r, self.user.username)

    def test_get_profile_articles(self) -> None:
        article = self.create_article(heading="article")
        article1 = self.create_article(heading="article1")
        article2 = self.create_article(heading="article2")

        cache.clear()
        url = reverse(
            "see_profile", kwargs={"username": self.user.username}
        )
        r = self.client.get(url)

        self.assertContains(r, article.heading)
        self.assertContains(r, article1.heading)
        self.assertContains(r, article2.heading)

    def test_change_pfp(self) -> None:
        with open("authentication/tests/cat.jpg", "rb") as pfp:
            new_pfp = SimpleUploadedFile(
                "cat.jpg", pfp.read(), content_type="image/jpeg"
            )

        url = reverse("change_pfp")
        self.client.post(
            url, {"new_pfp": new_pfp}, follow=True, format="multipart"
        )

        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.pfp)

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

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, username)

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

    # ========================
    # ====== Test utils ======
    # ========================
    def set_social_links(
        self, youtube: str = "https://www.youtube.com/",
        tiktok: str = "https://tiktok.com/",
        twitch: str = "https://twitch.tv/",
        linkedin: str = "https://linkedin.com/"
    ) -> HttpResponse:
        """Sets a passed social media links to the `self.user`
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
        self.user.refresh_from_db()

        return r
