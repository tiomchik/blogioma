from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status
from django.core.cache import cache

from main.utils import GenericTestCase


class UserTests(GenericTestCase):
    def test_register_without_username(self) -> None:
        user_data = {"password": "12341234"}
        r = self._register_user(**user_data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r.json().get("username"), ["This field is required."])

    def test_register_without_password(self) -> None:
        user_data = {"username": "test_user123"}
        r = self._register_user(**user_data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r.json().get("password"), ["This field is required."])

    def test_register_with_pfp(self) -> None:
        with open("authentication/tests/cat.jpg", "rb") as picture:
            pfp = SimpleUploadedFile(
                "cat.jpg", picture.read(), content_type="image/jpeg"
            )

        user_data = {
            "username": "test_user123",
            "password": "12341234",
            "pfp": pfp
        }
        url = reverse("register")
        r = self.client.post(url, user_data, format="multipart")
        self.user.refresh_from_db()

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(self.user.pfp)

    def test_me(self) -> None:
        url = reverse("me")
        r = self.client.get(url, headers={"Authorization": f"Token {self.token}"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json().get("username"), self.user.username)

    def test_me_without_auth(self) -> None:
        url = reverse("me")
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

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
        cache.clear()

        return r
