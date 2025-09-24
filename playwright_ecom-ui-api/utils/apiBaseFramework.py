from playwright.sync_api import Playwright
ordersPayLoad = {"orders":[{"country":"India","productOrderedId":"68a961459320a140fe1ca57a"}]}


class APIUtils:

    def getToken(self,playwright:Playwright,user_credentials):
        user_email = user_credentials['userEmail']
        userPassword = user_credentials['userPassword']
        api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com")
        try:
            response = api_request_context.post("/api/ecom/auth/login",
                                 data={"userEmail":user_email,"userPassword": userPassword})

            return response.status,response.json()
        finally:
            api_request_context.dispose()

    def login_api(self, playwright: Playwright, user_credentials):
        user_email = user_credentials['userEmail']
        userPassword = user_credentials['userPassword']
        api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com")
        try:
            response = api_request_context.post("/api/ecom/auth/login",
                                            data={"userEmail": user_email, "userPassword": userPassword},timeout=15000)

            return response.status, response.json()
        finally:
            api_request_context.dispose()

    def createOrder(self,playwright:Playwright,user_credentials, product_name="ZARA COAT 3", country="India"):
        status, body = self.getToken(playwright,user_credentials)
        token = body["token"]

        api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com")
        try:
            response = api_request_context.post("/api/ecom/order/create-order",
                                 data = ordersPayLoad,
                                 headers= {"Authorization": token,
                                           "Content-Type":"application/json"
                                           },timeout=15000)
            print(response.json())
            response_body = response.json()
            orderId = response_body["orders"][0]
            return orderId
        finally:
            api_request_context.dispose()

    def get_customer_products(self, playwright: Playwright, user_credentials):
        status, body = self.getToken(playwright, user_credentials)
        token = body["token"]
        userId = body["userId"]
        api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com")
        try:
            response = api_request_context.get(f"/api/ecom/order/get-orders-for-customer/{userId}",
                                           headers={"Authorization": token,
                                                    "Content-Type": "application/json"
                                                    })
            return response.status, response.json()
        finally:
            api_request_context.dispose()

    def delete_history_orders(self,playwright:Playwright,user_credentials):
        status, body = self.getToken(playwright, user_credentials)
        token = body["token"]
        api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com")

        created_order_Id = self.createOrder(playwright, user_credentials)

        # status_del, body_del = self.get_customer_products(playwright, user_credentials)
        # orderId = body_del["data"][0]["_id"]

        try:
            response = api_request_context.delete(f"/api/ecom/order/delete-order/{created_order_Id}",
                                              headers={"Authorization": token,
                                                       "Content-Type": "application/json"
                                                       })
            return response.status, response.json(), created_order_Id
        finally:
            api_request_context.dispose()