from pages.base_page import BasePage
from pages.order_page import OrderPage
from playwright.sync_api import Locator


class CartPage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)
        self.endpoint = "cart?action=show"

        self.product_list = self.page.get_by_label("Products in cart")
        self.proceed_to_checkout_button = self.page.get_by_role(
            "link", name="Proceed to checkout"
        )

    def get_product(self, product_id: int, product_attribute_id: int) -> Locator:
        return self.product_list.get_by_role("listitem").filter(
            has=self.page.locator(
                f'[data-id-product="{product_id}"]'
                f'[data-id-product-attribute="{product_attribute_id}"]'
            )
        )

    def proceed_to_checkout(self) -> OrderPage:
        self.proceed_to_checkout_button.click()
        return OrderPage(self.page)
