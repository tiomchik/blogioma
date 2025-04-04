from .generic import FeedbackGenericTestCase


class FeedbackTests(FeedbackGenericTestCase):
    data = {
        "email": "test@example.com",
        "problem": "lorem ipsum dolor",
        "problem_desc": "lorem ispum dolor"
    }

    def test_feedback(self) -> None:
        r = self.post_feedback(self.data)
        self.assertContains(r, "Message have been sent. We contact you soon.")
