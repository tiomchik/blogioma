from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from articles.models import Article
from authentication.models import Profile
from api.serializers import ReportSerializer
from feedback.models import Report


class ReportArticle(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, **kwargs) -> Report:
        report = Report.objects.create(**kwargs)
        article: Article = kwargs.pop("reported_article")
        article.reports.add(report)

        return report

    def post(self, request: Request, *args, **kwargs) -> Response:
        obj = get_object_or_404(Article.objects.all(), pk=kwargs.get("pk"))
        owner = Profile.objects.get(user=request.user)

        report_dict = {
            "reported_article": obj, "owner": owner,
            "reason": request.data.get("reason"),
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
