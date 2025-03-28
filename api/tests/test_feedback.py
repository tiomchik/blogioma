from django.urls import reverse

from main.generic_test_cases import APIGenericTestCase


class FeedbackTests(APIGenericTestCase):
    url = reverse("feedback-api")
    data = {
        "email": "test@test.com",
        "problem": "test",
        "problem_desc": "test"
    }

    def test_feedback(self) -> None:
        r = self.client.post(self.url, data=self.data)
        self.assertOkStatus(r)

    def test_empty_feedback(self) -> None:
        r = self.client.post(self.url, data={})
        self.assertFieldIsRequiredInJson(r, "email")
        self.assertFieldIsRequiredInJson(r, "problem")
        self.assertFieldIsRequiredInJson(r, "problem_desc")
