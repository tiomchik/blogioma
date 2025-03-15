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
        r = self.post_feedback(self.data)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Message have been sent. We contact you soon.")
