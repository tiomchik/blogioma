from rest_framework import serializers


class FeedbackSerializer(serializers.Serializer):
    email = serializers.EmailField()
    problem = serializers.CharField()
    problem_desc = serializers.CharField()
