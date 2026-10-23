from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)

        self.product_title = self.page.locator(".product__name")
        self.add_to_cart_button = self.page.get_by_role("button", name="Add to cart")
        self.black_color_option = self.page.locator(".product-variant__color").filter(
            has=page.get_by_text("Color - Black", exact=True)
        )
        self.inner_black_color_button = self.black_color_option.get_by_role("radio")
        self.size_dropdown = self.page.get_by_label("Size")
