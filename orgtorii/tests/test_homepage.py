from unittest import skip

from .playwright import PlaywrightTestCase

# Persona:
# Jane is a curious developer who likes to try out new orgtorii products.


@skip("Coming soon page is live")
class HomepageTestCase(PlaywrightTestCase):
    def test_homepage(self):
        # Jane hears of a new orgtorii product and wants to check out the homepage
        context = self.browser.new_context()  # Create an isolated browser context
        page = context.new_page()
        page.goto(self.server_url)
        self.assertIn("orgtorii", page.title())
