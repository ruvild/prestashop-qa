from typing import TYPE_CHECKING
from playwright.sync_api import Page
from typing import Self
from config.utils import url_joiner, get_env

if TYPE_CHECKING:
    from pages.login_page import LoginPage


class BasePage:

    def __init__(self, page: Page) -> None:
        self.endpoint = ""
        self.base_url = get_env("BASE_URL")
        self.page = page

        self.sign_in_header = page.get_by_label("Sign in")
        self.account_header = page.get_by_label("View my account")
        self.sign_out_link = page.locator(
            '[aria-labelledby="userMenuButton"]'
        ).get_by_role("link", name="Sign out")

        self.top_menu = page.get_by_label("Main navigation")
        self.category_button = self.top_menu.get_by_role("link").first
        self.category_sublink = (
            self.top_menu.get_by_role("tablist").get_by_role("link").first
        )

        self.search_bar = page.get_by_placeholder("Search")
        self.search_results_list = page.get_by_label("Search results")
        self.searched_products = self.search_results_list.get_by_role("option")

    @property
    def url(self) -> str:
        return url_joiner(self.base_url, self.endpoint)

    def navigate(self) -> Self:
        self.page.goto(self.url)
        return self

    def go_to_login_page(self) -> LoginPage:
        from pages.login_page import LoginPage

        self.sign_in_header.click()
        return LoginPage(self.page)

    def log_out(self) -> Self:
        self.account_header.click()
        self.sign_out_link.click()
        return self

    def expand_category_top_menu(self) -> Self:
        self.category_button.hover()
        return self

    def search_product(self, product_name: str) -> Self:
        self.search_bar.fill(product_name)
        return self
