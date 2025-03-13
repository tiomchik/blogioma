from feedback.models import Report
from .generic import FeedbackGenericTestCase


class ReportTests(FeedbackGenericTestCase):
    desc = "lorem ipsum dolor"

    def test_report(self) -> None:
        r = self.post_report(desc=self.desc)

        self.assertEqual(r.status_code, 200)
        self.assertTrue(
            Report.objects.filter(
                reported_article=self.article, desc=self.desc
            ).exists()
        )

    def test_unauth_report(self) -> None:
        self.client.logout()
        self.post_report(desc=self.desc)

        self.assertFalse(
            Report.objects.filter(
                reported_article=self.article, desc=self.desc
            ).exists()
        )
