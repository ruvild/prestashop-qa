from typing import Self

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage
from pages.order_page import OrderPage


class CartPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.endpoint = "cart?action=show"

        self.product_list = self.page.get_by_label("Products in cart")
        self.empty_cart_message = self.page.locator(".cart__empty")
        self.cart_summary = self.page.locator(".cart-summary")
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

    def get_quantity_input(self, product_id: int, product_attribute_id: int) -> Locator:
        return self.get_product(product_id, product_attribute_id).get_by_role(
            "textbox", name="Change quantity"
        )

    def increase_product_quantity(
        self, product_id: int, product_attribute_id: int
    ) -> Self:
        self.get_product(product_id, product_attribute_id).get_by_role(
            "button", name="Increase quantity"
        ).click()
        return self

    def decrease_product_quantity(
        self, product_id: int, product_attribute_id: int
    ) -> Self:
        self.get_product(product_id, product_attribute_id).get_by_role(
            "button", name="Decrease quantity"
        ).click()
        return self

    def remove_product(self, product_id: int, product_attribute_id: int) -> Self:
        self.get_product(product_id, product_attribute_id).get_by_role(
            "link", name="Remove"
        ).click()
        return self

    def proceed_to_checkout(self) -> OrderPage:
        self.proceed_to_checkout_button.click()
        return OrderPage(self.page)
