from playwright.sync_api import expect


class OrderDetailsPage:
    def __init__(self,page):
        self.page = page

    def verifyOrderMessage(self):
        expect(self.page.locator(".tagline")).to_contain_text("Thank you for Shopping With Us")