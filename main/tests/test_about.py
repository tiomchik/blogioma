from .generic import MainGenericTestCase


class AboutTests(MainGenericTestCase):
    def test_about(self) -> None:
        r = self.get_about_page()
        self.assertContains(r, "About")
