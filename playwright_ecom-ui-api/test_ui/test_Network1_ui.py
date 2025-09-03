import time

import pytest
pytestmark = pytest.mark.ui
from playwright.sync_api import Page


fakePayloadOrderResponse = {"data":[],"message":"No Orders"}

def intercept_response(route):
    route.fulfill(
        json= fakePayloadOrderResponse
    )
@pytest.mark.network_edge
def test_Network_no_orders(page:Page):
    page.goto("https://rahulshettyacademy.com/client")
    page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-for-customer/*",
                 intercept_response)
    page.get_by_placeholder("email@example.com").fill("test915@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("Test12345")
    page.get_by_role("button", name="Login").click() # api call from browser
    page.get_by_role("button",name="ORDERS").click()
    order_text = page.locator(".mt-4").text_content()
    assert order_text.strip() == "You have No Orders to show at this time. Please Visit Back Us"
    timeout = 10_000