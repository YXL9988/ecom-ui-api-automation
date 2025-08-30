import json
import pytest
from playwright.sync_api import Playwright,Page
from utils.apiBaseFramework import APIUtils
from pathlib import Path
pytestmark = pytest.mark.network

script_dir = Path(__file__).resolve().parent
data_file_path = script_dir.parent / "data" / "credentials.json"
with open(data_file_path) as f:
    test_data = json.load(f)
    user_credential_list = test_data['user_credentials']

@pytest.mark.parametrize('user_credentials',user_credential_list)
def test_orders_api_request(playwright:Playwright,page:Page,user_credentials):
    api = APIUtils()
    status,body=api.login_api(playwright, user_credentials)
    gettoken = body["token"]
    page.add_init_script(f"""localStorage.setItem('token','{gettoken}')""")
    page.goto("https://rahulshettyacademy.com/client")

    with page.expect_request("**/get-orders-for-customer/**") as req_info:
        page.get_by_role("button", name="ORDERS").click()

    request = req_info.value
    assert "get-orders-for-customer" in request.url

@pytest.mark.parametrize('user_credentials',user_credential_list)
def test_orders_api_response(playwright:Playwright,page:Page,user_credentials):
    api = APIUtils()
    status, body = api.login_api(playwright, user_credentials)
    gettoken = body["token"]
    page.add_init_script(f"""localStorage.setItem('token','{gettoken}')""")
    page.goto("https://rahulshettyacademy.com/client")

    with page.expect_response("**/get-orders-for-customer/**") as resp_info:
        page.get_by_role("button", name="ORDERS").click()

    response = resp_info.value
    assert response.status == 200
    data = response.json()
    order_ids = [order["_id"] for order in data["data"]]
    assert len(order_ids) > 0
    print("Captured Order IDs:", order_ids)




