from rest_framework import serializers

from .user import UserSerializer
from feedback.models import Report


class ReportSerializer(serializers.ModelSerializer):
    reported_article = serializers.HiddenField(default=None)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = "__all__"
