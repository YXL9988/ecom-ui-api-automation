from .orderDetails import OrderDetailsPage

class OrderHistoryPage:

    def __init__(self, page):
        self.page = page

    def selectOrder(self,orderId):
        row = self.page.locator("tr").filter(has_text=orderId)
        row.get_by_role("button", name="View").click()
        orderDetailsPage = OrderDetailsPage(self.page)
        return orderDetailsPage

    def get_all_order_ids(self):
        self.page.wait_for_selector("table tbody tr")
        return self.page.locator("table tbody th[scope='row']").all_text_contents()

    def is_order_present(self, order_id):
        order_ids = self.get_all_order_ids()
        print("UI Order IDs:", order_ids)
        return order_id in order_ids