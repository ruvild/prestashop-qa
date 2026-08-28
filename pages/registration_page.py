from pages.base_page import BasePage
from schemas.customer_schemas import CustomerRegistrationUI
from typing import Self


class RegistrationPage(BasePage):

    def __init__(self, page) -> None:
        super().__init__(page)
        self.endpoint = "registration"

        self.gender_mr = self.page.get_by_role("radio", name="Mr.")
        self.first_name = self.page.get_by_role("textbox", name="First name")
        self.last_name = self.page.get_by_role("textbox", name="Last name")
        self.email = self.page.get_by_role("textbox", name="Email", exact=True)
        self.password = self.page.get_by_role("textbox", name="Password")
        self.birthdate = self.page.get_by_role("textbox", name="Birthdate")
        self.offers = self.page.locator("#field-optin")
        self.customer_privacy = self.page.locator("#field-customer_privacy")
        self.terms_and_conditions = self.page.locator("#field-psgdpr")
        self.newsletter = self.page.locator("#field-newsletter")
        self.create_account = self.page.get_by_role("button", name="Create account")

    def register_valid(
        self, customer: CustomerRegistrationUI, optionals: bool = False
    ) -> BasePage:
        self.first_name.fill(customer.first_name)
        self.last_name.fill(customer.last_name)
        self.email.fill(customer.email)
        self.password.fill(customer.password)
        self.customer_privacy.check()
        self.terms_and_conditions.check()

        if optionals:
            self.gender_mr.check()
            self.birthdate.fill(customer.birthdate)
            self.offers.click()
            self.newsletter.click()

        self.create_account.click()
        return BasePage(self.page)

    def register_empty(self) -> Self:
        self.create_account.click()
        return self
