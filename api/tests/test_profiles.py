from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status

from main.utils import GenericTestCase


class UserTests(GenericTestCase):
    def test_change_username(self) -> None:
        data = {"username": "updated_test_user"}
        url = reverse("edit-me")
        r = self.client.put(
            url, data, headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertContains(r, data["username"])

    def test_change_password(self) -> None:
        previous_password = self.user.password
        data = {"password": "new_password"}
        url = reverse("edit-me")
        r = self.client.put(
            url, data, headers={"Authorization": f"Token {self.token}"}
        )

        self.user.refresh_from_db()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertNotEqual(previous_password, self.user.password)

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

    # ========================
    # ====== Test utils ======
    # ========================
    def _set_social_links(
        self, youtube: str = "https://www.youtube.com/",
        tiktok: str = "https://tiktok.com/",
        twitch: str = "https://twitch.tv/",
        linkedin: str = "https://linkedin.com/"
    ) -> HttpResponse:
        """Sets a social links to the `self.user` using PUT."""
        url = reverse("edit-me")
        data = {
            "youtube": youtube, "tiktok": tiktok,
            "twitch": twitch, "linkedin": linkedin
        }
        r = self.client.put(
            url, data, headers={"Authorization": f"Token {self.token}"}
        )
        self.user.refresh_from_db()

        return r

