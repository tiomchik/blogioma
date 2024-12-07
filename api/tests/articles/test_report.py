from rest_framework import status
from django.urls import reverse

from feedback.models import Report
from .generic import ArticleGenericTestCase


class ReportArticleTests(ArticleGenericTestCase):
    def test_report(self) -> None:
        url = self._get_report_article_url()
        r = self.client.post(
            url, {"reason": "Scam"},
            headers={"Authorization": f"Token {self.token}"}
        )

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        report = Report.objects.get(pk=r.json().get("id"))
        self.assertIsNotNone(self.article.reports.get(pk=report.pk))

    def test_unauth_report(self) -> None:
        url = self._get_report_article_url()
        r = self.client.post(url, {"reason": "Scam"})

        self._check_unauth_response(r)

    def _get_report_article_url(self) -> str:
        return reverse("report-article", kwargs={"pk": self.article.pk})
