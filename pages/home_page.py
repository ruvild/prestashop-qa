from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)

        self.carousel = page.get_by_label("Carousel container")
        self.featured_products = page.locator(".ps-featuredproducts")
        self.special_deals = page.locator(".ps-specials")
