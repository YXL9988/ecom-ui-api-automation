import os
import pytest
pytestmark = pytest.mark.ui

HEADLESS = os.getenv("HEADLESS", "1") not in ("0", "false", "False")

from playwright.sync_api import Page, expect, Playwright

def test_playwrightBasics(playwright):
    browser = playwright.chromium.launch(headless=HEADLESS)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/client")

def test_playwrightShortCut(page:Page): #fixture(page) comes from class(Page)
    page.goto("https://rahulshettyacademy.com/client", wait_until="domcontentloaded", timeout=60000)

def test_coreLocators(page:Page):
    page.goto("https://rahulshettyacademy.com/client")
    page.locator("#userEmail").fill("test915@gmail.com")
    #page.get_by_role("textbox",name="Email").fill("test915@gmail.com") #type
    page.locator("#userPassword").fill("Test12345")
    login_btn = page.locator("#login")
    expect(login_btn).to_be_visible()
    login_btn.click()

def test_firefoxBrowser(playwright:Playwright):
    firefoxBrowser = playwright.firefox.launch(headless=HEADLESS)
    page = firefoxBrowser.new_page()
    page.goto("https://rahulshettyacademy.com/client")
    page.locator("#userEmail").fill("test915@gmail.com")
    page.locator("#userPassword").fill("Test12345")
    login_btn = page.locator("#login")
    expect(login_btn).to_be_visible()
    login_btn.click()

def test_delete_products_history(page:Page):
    page.goto("https://rahulshettyacademy.com/client")
    page.locator("#userEmail").fill("test915@gmail.com")
    # page.get_by_role("textbox",name="Email").fill("test915@gmail.com") #type
    page.locator("#userPassword").fill("Test12345")
    page.locator("#login").click()

    page.get_by_role("button",name="ORDERS").click()
    page.wait_for_url("**/myorders", timeout=10000)
    page.wait_for_load_state("networkidle")

    rows = page.locator("tbody tr")
    before = rows.count()
    first_row = rows.first
    order_id = first_row.locator("th").inner_text().strip()
    print(order_id)

    page.get_by_role("button",name="Delete").first.click()
    #page.get_by_role("button",name="Delete").nth(0).click()
    expect(rows.filter(has_text=order_id)).to_have_count(0)
    expect(rows).to_have_count(before - 1)

