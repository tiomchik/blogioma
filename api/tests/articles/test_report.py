from rest_framework import status

from feedback.models import Report
from .generic import ArticleGenericTestCase


class ReportArticleTests(ArticleGenericTestCase):
    report_data = {"reason": "Scam"}

    def test_report(self) -> None:
        r = self.report_article(self.report_data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        report = Report.objects.get(pk=r.json().get("id"))
        self.assertIsNotNone(self.article.reports.get(pk=report.pk))

    def test_unauth_report(self) -> None:
        self.auth_header = {}
        r = self.report_article(self.report_data)
        self.assertUnauthResponse(r)
