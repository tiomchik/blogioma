from feedback.models import Report
from .generic import FeedbackGenericTestCase


class ReportTests(FeedbackGenericTestCase):
    def test_report(self) -> None:
        desc = "lorem ipsum dolor"
        r = self.post_report(desc=desc)

        self.assertEqual(r.status_code, 200)
        self.assertTrue(
            Report.objects.filter(
                reported_article=self.article, desc=desc
            ).exists()
        )

    def test_unauth_report(self) -> None:
        self.client.logout()
        desc = "lorem ipsum dolor"
        self.post_report(desc=desc)

        self.assertFalse(
            Report.objects.filter(
                reported_article=self.article, desc=desc
            ).exists()
        )
