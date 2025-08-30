import pytest
pytestmark = pytest.mark.ui
from playwright.sync_api import Page, expect
import re

@pytest.mark.site_angular
def test_add_to_cart_UIValidationDynamicScript(page:Page):
    #iphone X, Nokia Edge -> verify 2 items are showing in cart.
    page.goto("https://rahulshettyacademy.com/angularpractice/shop")
    iphoneProduct = page.locator("app-card").filter(has_text="iphone X")
    iphoneProduct.get_by_role("button").click()
    nokiaProduct = page.locator("app-card").filter(has_text="Nokia Edge")
    nokiaProduct.get_by_role("button").click()
    page.get_by_text("Checkout").click()
    expect(page.locator(".media-body")).to_have_count(2)

@pytest.mark.site_angular
def test_add_all_items_to_cart(page:Page):
    page.goto("https://rahulshettyacademy.com/angularpractice/shop")
    products = page.locator("app-card")
    totalAdded = products.count()
    for i in range (totalAdded):
        products.nth(i).get_by_role("button",name="Add").click()

    page.get_by_role("link", name=re.compile(r"^Checkout"))
    page.locator(".nav-link.btn.btn-primary").click()
    product_column = page.locator("h4.media-heading a")
    expect(product_column).to_have_count(totalAdded)

@pytest.mark.site_angular
@pytest.mark.childwindow
def test_childWindowHandle(page:Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")

    with page.expect_popup() as newPage_info:
        page.locator(".blinkingText").nth(0).click()
        childPage = newPage_info.value
        childPage.locator("Protractor Tutorial")
        text = childPage.locator(".red").text_content()
        print(text)
        words = text.split("at")
        email = words[1].strip().split(" ")[0]
        assert email == "mentor@rahulshettyacademy.com" #pytest assertion

