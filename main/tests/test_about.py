from django.urls import reverse

from main.generic_test_cases import GenericTestCase


class AboutTests(GenericTestCase):
    url = reverse("about")

    def test_about(self) -> None:
        r = self.client.get(self.url)
        self.assertContains(r, "About")
