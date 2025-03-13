from django.urls import reverse
from urllib.parse import urlencode

from .generic import FeedbackGenericTestCase


class FeedbackTests(FeedbackGenericTestCase):
    data = {
        "email": "test@example.com",
        "problem": "lorem ipsum dolor",
        "problem_desc": "lorem ispum dolor"
    }

    def test_feedback(self) -> None:
        url = reverse("feedback")
        r = self.client.post(
            url, urlencode(self.data),
            content_type="application/x-www-form-urlencoded", follow=True
        )

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Message have been sent. We contact you soon.")
