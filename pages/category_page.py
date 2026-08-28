from pages.base_page import BasePage


class CategoryPage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)

        self.filter_block = self.page.get_by_role("region", name="Filter")
        self.product_section = self.page.locator("#products")
        self.filtered_products = self.product_section.locator("[data-id-product]")
