from django.core.cache import cache
from django.urls import reverse
from django.http import HttpResponse

from main.utils import GenericTestCase


class AuthenticationGenericTestCase(GenericTestCase):
    def _set_social_links(
        self,
        youtube: str = "https://www.youtube.com/",
        tiktok: str = "https://tiktok.com/",
        twitch: str = "https://twitch.tv/",
        linkedin: str = "https://linkedin.com/"
    ) -> HttpResponse:
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
