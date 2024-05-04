from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request

from articles.models import Article
from api.serializers import ReportSerializer
from feedback.models import Report


class ReportArticle(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            obj = Article.objects.get(pk=kwargs.get("pk"))
        except Article.DoesNotExist:
            return Response(
                {"detail": "No article matches the given query."},
                status=status.HTTP_404_NOT_FOUND, exception=True
            )

        report_dict = {
            "reported_article": obj, "reason": request.data.get("reason"),
            "desc": request.data.get("desc")
        }

        serializer = ReportSerializer(data=report_dict)
        serializer.is_valid(raise_exception=True)
        report = self.perform_create(**report_dict)

        headers = self.get_success_headers(serializer.data)
        return Response(
            ReportSerializer(report).data, status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, **kwargs) -> Report:
        report = Report.objects.create(**kwargs)
        article: Article = kwargs.pop("reported_article")
        article.reports.add(report)

        return report
