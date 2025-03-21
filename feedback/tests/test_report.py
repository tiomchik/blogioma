from .generic import FeedbackGenericTestCase


class ReportTests(FeedbackGenericTestCase):
    data = {
        "reason": "Scam",
        "desc": "lorem ipsum dolor"
    }

    def test_report(self) -> None:
        self.post_report(self.data)
        self.assertReportExists(reported_article=self.article, **self.data)

    def test_unauth_report(self) -> None:
        self.client.logout()
        self.post_report(self.data)
        self.assertReportDoesntExists(
            reported_article=self.article, **self.data
        )
