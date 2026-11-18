from pages.base_page import BasePage
from config.utils import extract_product_ids


class CategoryPage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)

        self.filter_block = self.page.get_by_role("region", name="Filter")
        self.product_section = self.page.locator("#products")
        self.filtered_products = self.product_section.locator("[data-id-product]")

    def get_filtered_products_ids(self) -> set[int]:
        filtered_products_ids_ui = [
            product.get_attribute("data-id-product")
            for product in self.filtered_products.all()
        ]
        return set(extract_product_ids(filtered_products_ids_ui))
