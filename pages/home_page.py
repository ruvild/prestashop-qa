from pages.base_page import BasePage
from playwright.sync_api import Locator
from pages.product_page import ProductPage


class HomePage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)

        self.carousel = page.get_by_label("Carousel container")
        self.featured_products_block = page.locator(".ps-featuredproducts")
        self.special_deals_block = page.locator(".ps-specials")
        self.latest_arrivals_block = page.locator(".ps-newproducts")
        self.featured_product = self.featured_products_block.locator(
            "[data-id-product='1']"
        )

        self.quick_view_button = self.featured_product.get_by_role(
            "button", name="Quick view"
        )
        self.quick_view_dialog = page.locator(".quickview__dialog")
        self.quick_view_product_title = self.quick_view_dialog.locator(".product__name")
        self.all_product_details = self.quick_view_dialog.get_by_text("All details")

    def get_featured_product(self) -> Locator:
        return self.featured_product

    def get_new_product(self, product_id: int) -> Locator:
        return self.latest_arrivals_block.locator(f"[data-id-product='{product_id}']")

    def open_quick_view(self) -> Locator:
        self.featured_product.hover()
        self.quick_view_button.click()
        return self.quick_view_dialog

    def navigate_to_product_page(self, product_locator: Locator) -> ProductPage:
        product_locator.click()
        return ProductPage(self.page)

    def navigate_to_product_page_via_quick_view(self) -> ProductPage:
        self.all_product_details.click()
        return ProductPage(self.page)
