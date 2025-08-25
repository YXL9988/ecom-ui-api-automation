import pytest
pytestmark = pytest.mark.ui

import time

import pytest
from playwright.sync_api import Page, Playwright,expect

from utils.apiBase import APIUtils


def intercept_Request(route): #mocking the request
    route.continue_(url="https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=68a6fe44d2e3f0f153bd87f1")
    #input different user's "_id" (Order Id)

@pytest.mark.smoke
def test_Network_unauthorized_user(page:Page):
    page.goto("https://rahulshettyacademy.com/client")
    page.route("https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=*",
               intercept_Request)
    page.get_by_placeholder("email@example.com").fill("test915@gmail.com")
    page.get_by_placeholder("enter your passsword").fill("Test12345")
    page.get_by_role("button", name="Login").click() # api call from browser
    page.get_by_role("button",name="ORDERS").click()
    page.get_by_role("button", name="View").first.click()
    time.sleep(5)
    message = page.locator(".blink_me").text_content()
    print(message) #You are not authorize to view this order
    time.sleep(5)

def test_session_storage_bypass_login(playwright:Playwright):
    api_utils = APIUtils()
    gettoken = api_utils.getToken(playwright)
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    #script to inject token in session local storage
    page.add_init_script(f"""localStorage.setItem('token','{gettoken}')""")
    page.goto("https://rahulshettyacademy.com/client") #bypass login process
    page.get_by_role("button", name="ORDERS").click()
    expect(page.get_by_text("Your Orders")).to_be_visible()