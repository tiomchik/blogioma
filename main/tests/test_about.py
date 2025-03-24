from django.urls import reverse

from main.generic_test_cases import SessionAuthGenericTestCase


class AboutTests(SessionAuthGenericTestCase):
    url = reverse("about")

    def test_about(self) -> None:
        r = self.client.get(self.url)
        self.assertContains(r, "About")
