import os

import pytest
pytestmark = pytest.mark.ui
from playwright.sync_api import Page, expect

def _login(page:Page):
    page.goto("https://rahulshettyacademy.com/client")
    page.locator("#userEmail").fill("test915@gmail.com")
    page.locator("#userPassword").fill("Test12345")
    page.locator("#login").click()

def _cards(page:Page):
    return page.locator("app-card, section#products .card")

def test_filter_search_by_text(page: Page):
    _login(page)
    page.goto("https://rahulshettyacademy.com/client/#/dashboard/dash")

    search = page.get_by_role("textbox",name="search")
    search.fill("ZARA")
    search.press("Enter")
    page.wait_for_load_state("networkidle")

    expect(_cards(page).filter(has_text="ZARA")).to_have_count(1)
    expect(_cards(page).filter(has_text="ADIDAS")).to_have_count(0)
    expect(_cards(page).filter(has_text="iphone 13 pro")).to_have_count(0)

@pytest.mark.skipif(os.getenv("CI"), reason="external site data may vary on CI")
def test_filter_price_range(page:Page):
    _login(page)
    page.goto("https://rahulshettyacademy.com/client/#/dashboard/dash")

    page.get_by_role("textbox",name="Min Price").fill("0")
    page.get_by_role("textbox",name="Max Price").fill("20000")
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")

    expect(_cards(page).filter(has_text="iphone 13 pro")).to_have_count(0)
    expect(_cards(page)).not_to_have_count(0)
