import json
import pytest
pytestmark = pytest.mark.api
from pathlib import Path
from playwright.sync_api import Playwright
from pageObject.login import LoginPage
from utils.apiBaseFramework import APIUtils
import time

ordersPayLoad = {"orders":[{"country":"India","productOrderedId":"68a961459320a140fe1ca57a"}]}

script_dir = Path(__file__).resolve().parent
# Construct the absolute path to the data file
data_file_path = script_dir.parent / "data" / "credentials.json"
with open(data_file_path) as f:
    test_data = json.load(f)  # convert json into python object
    user_credential_list = test_data['user_credentials']

data_file_path = script_dir.parent / "data" / "credentials_negative.json"
with open(data_file_path) as k:
    test_data = json.load(k)
    user_credential_list_negative = test_data['user_credentials_negative']

@pytest.mark.happy
@pytest.mark.parametrize('user_credentials',user_credential_list)
def test_api_login_access_api(playwright:Playwright,user_credentials):
    api = APIUtils()
    status, response = api.login_api(playwright,user_credentials)
    assert status == user_credentials["expected"]
    if status == 200:
        assert "token" in response
        assert response["message"] == "Login Successfully"


@pytest.mark.parametrize('user_credentials_negative',user_credential_list_negative)
def test_api_login_access_negative_api(playwright:Playwright,user_credentials_negative):
    api = APIUtils()
    status, response = api.login_api(playwright, user_credentials_negative)
    assert status == user_credentials_negative["expected"]
    if status == 400:
        assert "message" in response
        assert "Incorrect email or password." in response["message"]

@pytest.mark.happy
@pytest.mark.parametrize('user_credentials', user_credential_list)
def test_get_orders_api(playwright: Playwright, user_credentials):
    api_utils = APIUtils()
    order_id = api_utils.createOrder(playwright, user_credentials)
    status,body = api_utils.get_customer_products(playwright, user_credentials)
    assert status == 200
    orders = body["data"]
    assert any(order["_id"] == order_id for order in orders)

@pytest.mark.parametrize("bad_token", [None,"", "invalid123", "Bearer abc.def.ghi"])
def test_create_order_invalid_token_api(playwright:Playwright, bad_token):
    headers = {}
    if bad_token is not None:
        headers["Authorization"] = bad_token
    invalid_token = playwright.request.new_context(
        base_url="https://rahulshettyacademy.com",
        extra_http_headers=headers
    )
    response = invalid_token.post("/api/ecom/order/create-order",
                                  data = ordersPayLoad)
    body = response.json()
    assert response.status == 401
    assert "message" in body

@pytest.mark.parametrize('user_credentials',user_credential_list)
def test_create_order_missing_payload_api(playwright, user_credentials):
    api_utils=APIUtils()
    status, body = api_utils.getToken(playwright, user_credentials)
    valid_token = body["token"]

    missing_payload = playwright.request.new_context(
        base_url="https://rahulshettyacademy.com",
        extra_http_headers={"Authorization": valid_token})

    response = missing_payload.post("/api/ecom/order/create-order",data ={})
    body = response.json()
    assert response.status == 500
    assert "message" in body

@pytest.mark.happy
@pytest.mark.smoke
@pytest.mark.parametrize('user_credentials',user_credential_list) #pass the data to fixture in conftest
def test_e2e_web_api(playwright:Playwright, browserInstance, user_credentials,app_url):
    userEmail = user_credentials["userEmail"]
    userPassword = user_credentials["userPassword"]

    #create order -> orderId
    api_utils = APIUtils()
    orderId = api_utils.createOrder(playwright,user_credentials)

    #login
    loginPage = LoginPage(browserInstance)
    loginPage.navigate(app_url)
    dashboardPage = loginPage.login(userEmail,userPassword)
    #DashBoard Page
    orderHistoryPage = dashboardPage.selectOrdersNavLink()
    orderDetailsPage = orderHistoryPage.selectOrder(orderId)
    orderDetailsPage.verifyOrderMessage()

@pytest.mark.smoke
@pytest.mark.parametrize('user_credentials',user_credential_list)
def test_check_orderId(playwright:Playwright, browserInstance, user_credentials,app_url):
    userEmail = user_credentials["userEmail"]
    userPassword = user_credentials["userPassword"]

    # create order -> orderId
    api_utils = APIUtils()
    orderId = api_utils.createOrder(playwright, user_credentials)
    print("created orderId:", orderId)

    # login
    loginPage = LoginPage(browserInstance)
    loginPage.navigate(app_url)
    dashboardPage = loginPage.login(userEmail, userPassword)
    orderHistoryPage = dashboardPage.selectOrdersNavLink()

    # check orderId
    assert orderHistoryPage.is_order_present(orderId)

@pytest.mark.happy
@pytest.mark.parametrize('user_credentials',user_credential_list)
def test_api_get_customer_products_api(playwright:Playwright,user_credentials):
    api_utils = APIUtils()
    status, body = api_utils.get_customer_products(playwright,user_credentials)
    expected = user_credentials["expected"]
    assert status == expected
    assert "data" in body
    if "count" in body:
        assert body["count"] == len(body["data"])

@pytest.mark.parametrize('user_credentials',user_credential_list)
@pytest.mark.parametrize("bad_token", [None,"", "invalid123", "Bearer abc.def.ghi"])
def test_get_customer_products_invalid_token_api(playwright,user_credentials,bad_token):
    api_utils = APIUtils()
    status, body = api_utils.getToken(playwright, user_credentials)
    userId = body["userId"]

    headers = {}
    if bad_token is not None:
        headers["Authorization"] = bad_token

    invalid_token = playwright.request.new_context(
        base_url="https://rahulshettyacademy.com",
        extra_http_headers=headers
    )
    response = invalid_token.get(f"/api/ecom/order/get-orders-for-customer/{userId}")
    body = response.json()
    assert response.status == 401
    assert "message" in body

@pytest.mark.happy
@pytest.mark.parametrize('user_credentials',user_credential_list)
def test_delete_history_orders_api(playwright:Playwright,user_credentials):
    api_utils = APIUtils()
    status, body, deleted_order_id = api_utils.delete_history_orders(playwright, user_credentials)
    print(body.get("message"))
    assert status == 200
    assert body.get("message") == "Orders Deleted Successfully"

    status_check, body_check = api_utils.get_customer_products(playwright,user_credentials)
    order_ids = [o["_id"] for o in body_check["data"]]
    assert deleted_order_id not in order_ids

@pytest.mark.parametrize('user_credentials',user_credential_list)
@pytest.mark.parametrize("bad_token", [None,"", "invalid123", "Bearer abc.def.ghi"])
def test_delete_history_orders_invalid_token_api(playwright:Playwright,user_credentials,bad_token):
    api_utils = APIUtils()
    created_order_Id = api_utils.createOrder(playwright, user_credentials)

    headers = {}
    if bad_token is not None:
        headers["Authorization"] = bad_token
    invalid_token = playwright.request.new_context(
        base_url="https://rahulshettyacademy.com",
        extra_http_headers=headers
    )
    response = invalid_token.delete(f"/api/ecom/order/delete-order/{created_order_Id}")
    body = response.json()
    assert response.status == 401
    assert "message" in body