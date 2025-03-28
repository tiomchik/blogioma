from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.request import Request

from feedback.tasks import send_feedback
from api.serializers.feedback import FeedbackSerializer


class Feedback(views.APIView):
    serializer_class = FeedbackSerializer

    def post(self, request: Request) -> Response:
        serializer = self.validate_serializer(request.data)
        mail_data = self.prepare_mail_data(serializer.validated_data)
        self.send_feedback(mail_data)

        return self.create_success_response(serializer)

    def validate_serializer(self, data: dict) -> FeedbackSerializer:
        serializer = FeedbackSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def prepare_mail_data(self, validated_data: dict) -> tuple:
        mail_heading = self._get_formatted_mail_heading(
            validated_data["problem"]
        )
        mail_desc = self._get_formatted_mail_desc(
            validated_data["problem_desc"],
            validated_data["email"]
        )
        return mail_heading, mail_desc

    def _get_formatted_mail_heading(self, problem: str) -> str:
        return "Blogioma report: " + problem

    def _get_formatted_mail_desc(self, problem_desc: str, email: str) -> str:
        return problem_desc + f"\n\n\nUser email: {email}"

    def send_feedback(self, mail_data: tuple) -> None:
        send_feedback.delay(*mail_data)

    def create_success_response(self, serializer) -> Response:
        return Response(data=serializer.data, status=status.HTTP_200_OK)
