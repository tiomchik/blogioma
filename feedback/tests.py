from django.urls import reverse
from django.http import HttpResponse
from urllib.parse import urlencode

from main.utils import GenericTestCase
from .models import Report


class FeedbackTests(GenericTestCase):
    def setUp(self) -> None:
        self.setUpSessionAuth()

    def test_feedback(self) -> None:
        url = reverse("feedback")
        data = urlencode({
            "email": "test@example.com", "problem": "lorem ipsum dolor",
            "problem_desc": "lorem ispum dolor"
        })
        r = self.client.post(
            url, data, content_type="application/x-www-form-urlencoded",
            follow=True
        )

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Message have been sent. We contact you soon.")

    def test_report(self) -> None:
        desc = "lorem ipsum dolor"
        r = self._post_report(desc=desc)

        self.assertEqual(r.status_code, 200)
        self.assertTrue(
            Report.objects.filter(
                reported_article=self.article, desc=desc
            ).exists()
        )

    def test_unauth_report(self) -> None:
        self.client.logout()
        desc = "lorem ipsum dolor"
        self._post_report(desc=desc)

        self.assertFalse(
            Report.objects.filter(
                reported_article=self.article, desc=desc
            ).exists()
        )

    # ========================
    # ====== Test utils ======
    # ========================
    def _post_report(
        self, reason: str = "Scam", desc: str = "lorem ipsum dolor"
    ) -> HttpResponse:
        """Creates a report using POST."""
        data = urlencode({"reason": reason, "desc": desc})
        url = reverse("report", kwargs={"pk": self.article.pk})
        r = self.client.post(
            url, data, content_type="application/x-www-form-urlencoded",
            follow=True
        )

        return r
