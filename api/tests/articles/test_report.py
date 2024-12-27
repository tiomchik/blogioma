from rest_framework import status
from django.urls import reverse

from feedback.models import Report
from .generic import ArticleGenericTestCase


class ReportArticleTests(ArticleGenericTestCase):
    report_data = {"reason": "Scam"}

    def setUp(self):
        super().setUp()
        self.url = reverse("report-article", kwargs={"pk": self.article.pk})

    def test_report(self) -> None:
        r = self.client.post(
            self.url, self.report_data, headers=self.auth_header
        )
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        report = Report.objects.get(pk=r.json().get("id"))
        self.assertIsNotNone(self.article.reports.get(pk=report.pk))

    def test_unauth_report(self) -> None:
        r = self.client.post(self.url, self.report_data)
        self._assert_unauth_response(r)
