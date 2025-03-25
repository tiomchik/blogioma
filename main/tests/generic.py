from django.urls import reverse
from django.http import HttpResponse

from main.generic_test_cases import SessionAuthGenericTestCase


class MainGenericTestCase(SessionAuthGenericTestCase):
    def get_home_page(self) -> HttpResponse:
        url = reverse("home")
        r = self.client.get(url)
        return r

    def get_about_page(self) -> HttpResponse:
        url = reverse("about")
        r = self.client.get(url)
        return r
