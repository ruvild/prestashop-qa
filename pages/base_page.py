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
