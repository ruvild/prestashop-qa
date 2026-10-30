from pages.base_page import BasePage


class OrderConfirmationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.common_prefix = "order-confirmation__"
        self.order_confirmed_block = page.get_by_role("alert")
        self.order_details_block = page.locator(f".{self.common_prefix}details")

        self.order_reference = self.order_details_block.get_by_text("Order reference")
        self.payment_method = self.order_details_block.get_by_text("Payment method")
        self.shipping_method = self.order_details_block.get_by_text("Shipping method")
        self.product_title = self.order_details_block.locator(
            f".{self.common_prefix}product-title"
        )
        self.quantity = self.order_details_block.locator(
            f".{self.common_prefix}product-quantity"
        )
        self.total_value = self.order_details_block.locator(
            f".{self.common_prefix}totals"
        ).locator(f".{self.common_prefix}line-value")
