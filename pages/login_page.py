from pages.base_page import BasePage
from pages.registration_page import RegistrationPage
from typing import Self


class LoginPage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)
        self.endpoint = "login"

        self.email = self.page.get_by_role("textbox", name="Email", exact=True)
        self.password = self.page.get_by_role("textbox", name="Password")
        self.sign_in_button = self.page.get_by_role("button", name="Sign in")
        self.create_account_button = self.page.get_by_role(
            "link", name="Create your account"
        )
        self.auth_fail_alert = self.page.get_by_role("alert")

    def sign_in(self, email, password) -> BasePage:
        self.email.fill(email)
        self.password.fill(password)
        self.sign_in_button.click()
        return BasePage(self.page)

    def sign_in_with_invalid_password(self, email, password) -> Self:
        self.email.fill(email)
        self.password.fill(password + "e")
        self.sign_in_button.click()
        return self

    def create_account(self) -> RegistrationPage:
        self.create_account_button.click()
        return RegistrationPage(self.page)
