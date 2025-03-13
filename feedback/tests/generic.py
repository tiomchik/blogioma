from django.urls import reverse
from django.http import HttpResponse
from urllib.parse import urlencode

from main.utils import GenericTestCase


class FeedbackGenericTestCase(GenericTestCase):
    def setUp(self) -> None:
        self.setUpSessionAuth()

    def post_report(
        self, reason: str = "Scam", desc: str = "lorem ipsum dolor"
    ) -> HttpResponse:
        data = urlencode({"reason": reason, "desc": desc})
        url = reverse("report", kwargs={"pk": self.article.pk})
        r = self.client.post(
            url, data, content_type="application/x-www-form-urlencoded",
            follow=True
        )

        return r
