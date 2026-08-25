from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)

        self.product_title = self.page.locator(".product__name")
        self.add_to_cart_button = self.page.get_by_role("button", name="Add to cart")
