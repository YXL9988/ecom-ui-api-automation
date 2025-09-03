from playwright.sync_api import Playwright
ordersPayLoad = {"orders":[{"country":"India","productOrderedId":"68a86429b01c5d7abb27e634"}]}

class APIUtils:

    def getToken(self,playwright:Playwright):
        api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com")
        response = api_request_context.post("/api/ecom/auth/login",
                                 data={"userEmail":"linyanxi915@gmail.com","userPassword": "6Y7u8I9o"})
        assert response.ok
        print(response.json())
        responseBody = response.json()
        return responseBody["token"]

    def createOrder(self,playwright:Playwright):
        token = self.getToken(playwright)
        api_request_context = playwright.request.new_context(base_url="https://rahulshettyacademy.com")
        response = api_request_context.post("/api/ecom/order/create-order",
                                 data = ordersPayLoad,
                                 headers = {"Authorization": token,
                                           "Content-Type":"application/json"
                                           })
        print(response.json())
        response_body = response.json()
        orderId = response_body["orders"][0]
        return orderId
