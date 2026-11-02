from pages.base_page import BasePage
from pages.order_confirmation_page import OrderConfirmationPage
from typing import Self
from test_data.customer_test_data import AddressData


class OrderPage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)
        self.endpoint = "order"

        self.address = page.get_by_label("Address", exact=True)
        self.city = page.get_by_label("City")
        self.zipcode = page.get_by_label("Zip/Postal Code")
        self.country = page.get_by_label("Country")
        self.state = page.get_by_label("State")
        self.go_to_shipping_button = page.get_by_role("button", name="Continue")

        self.default_delivery_option = page.get_by_role("radio", name="My carrier")
        self.go_to_payment_button = page.get_by_role("button", name="Payment")

        self.wire_payment_option = page.get_by_role("radio", name="wire")
        self.tos_agreement = page.get_by_role("checkbox")
        self.place_order_button = page.get_by_role("button", name="order")

    def insert_address(self, address_data: AddressData) -> Self:
        self.country.select_option(label=address_data.country)
        self.state.select_option(label=address_data.state)
        self.address.fill(address_data.address)
        self.city.fill(address_data.city)
        self.zipcode.fill(address_data.zipcode)
        self.go_to_shipping_button.click()
        return self

    def proceed_to_payment(self) -> Self:
        self.go_to_payment_button.click()
        return self

    def place_order(self) -> OrderConfirmationPage:
        self.wire_payment_option.check()
        self.tos_agreement.check()
        self.place_order_button.click()
        return OrderConfirmationPage(self.page)
