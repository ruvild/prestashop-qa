from datetime import datetime

import pytest
from playwright.sync_api import expect
from requests import HTTPError

from factories.customer_factory import CustomerFactory
from pages.base_page import BasePage
from pages.registration_page import RegistrationPage
from test_data.customer_test_data import CustomerTestData


@pytest.mark.smoke
@pytest.mark.hybrid
def test_register_required_ui(page, cleanup_customer, customers_client):
    customer = CustomerFactory.create_required_ui()

    current_page = (
        BasePage(page)
        .navigate()
        .go_to_login_page_via_header()
        .create_account()
        .register_valid(customer)
    )

    expect(page).to_have_url(current_page.url)
    expect(current_page.account_header).to_be_visible()

    saved_customer = customers_client.search_customer_by_email(customer.email)
    cleanup_customer(saved_customer.idCustomer)

    assert saved_customer.firstname == customer.first_name
    assert saved_customer.lastname == customer.last_name
    assert saved_customer.email == customer.email


@pytest.mark.regression
@pytest.mark.ui
def test_register_empty_ui(page):
    current_page = RegistrationPage(page).navigate().register_empty()
    expect(page).to_have_url(current_page.url)
    expect(current_page.email).to_be_visible()
    expect(current_page.account_header).to_have_count(0)
    assert current_page.first_name.evaluate("el => el.validity.valueMissing") is True


@pytest.mark.regression
@pytest.mark.hybrid
def test_register_optionals_ui(page, cleanup_customer, customers_client):
    customer = CustomerFactory.create_full_ui()

    current_page = (
        RegistrationPage(page).navigate().register_valid(customer, optionals=True)
    )

    expect(page).to_have_url(current_page.url)
    expect(current_page.account_header).to_be_visible()

    search_result = customers_client.search_customer_by_email(customer.email)
    cleanup_customer(search_result.idCustomer)

    saved_customer = customers_client.get_customer(search_result.idCustomer)
    expected_birthday = (
        datetime.strptime(customer.birthdate, "%m/%d/%Y").date().isoformat()
    )

    assert saved_customer.firstName == customer.first_name
    assert saved_customer.lastName == customer.last_name
    assert saved_customer.email == customer.email
    assert saved_customer.genderId == 1
    assert saved_customer.birthday == expected_birthday
    assert saved_customer.newsletterSubscribed is True
    assert saved_customer.partnerOffersSubscribed is True


@pytest.mark.smoke
@pytest.mark.api
def test_register_required_api(cleanup_customer, customers_client):
    customer = CustomerFactory().create_required_api()

    customer_response = customers_client.create_customer(customer)
    cleanup_customer(customer_response.customerId)

    saved_customer = customers_client.get_customer(customer_response.customerId)
    assert saved_customer.firstName == customer.firstName
    assert saved_customer.lastName == customer.lastName
    assert saved_customer.email == customer.email
    assert saved_customer.defaultGroupId == customer.defaultGroupId
    assert set(saved_customer.groupIds) == set(customer.groupIds)
    assert saved_customer.enabled is True
    assert saved_customer.guest is False

    response_dict = customer_response.model_dump()
    assert "password" not in response_dict


@pytest.mark.regression
@pytest.mark.api
def test_register_full_api(customers_client, cleanup_customer):
    customer = CustomerFactory().create_full_api()

    customer_response = customers_client.create_customer(customer)
    cleanup_customer(customer_response.customerId)

    saved_customer = customers_client.get_customer(customer_response.customerId)
    assert saved_customer.firstName == customer.firstName
    assert saved_customer.lastName == customer.lastName
    assert saved_customer.email == customer.email
    assert saved_customer.defaultGroupId == customer.defaultGroupId
    assert set(saved_customer.groupIds) == set(customer.groupIds)
    assert saved_customer.genderId == customer.genderId
    assert saved_customer.partnerOffersSubscribed == customer.partnerOffersSubscribed
    assert saved_customer.birthday == customer.birthday
    assert saved_customer.companyName == customer.companyName
    assert saved_customer.siretCode == customer.siretCode
    assert saved_customer.apeCode == customer.apeCode
    assert saved_customer.website == customer.website
    assert saved_customer.allowedOutstandingAmount == customer.allowedOutstandingAmount
    assert saved_customer.maxPaymentDays == customer.maxPaymentDays
    assert saved_customer.riskId == customer.riskId

    response_dict = customer_response.model_dump()
    assert "password" not in response_dict


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.xfail(
    reason="BUG: Admin API POST /customers ignores newsletterSubscribed (missing COMMAND_MAPPING)",
    strict=True,
)
def test_register_newsletter_subscription_api(customers_client, cleanup_customer):
    customer = CustomerFactory().create_required_api()
    customer.newsletterSubscribed = True

    customer_response = customers_client.create_customer(customer)
    cleanup_customer(customer_response.customerId)

    saved_customer = customers_client.get_customer(customer_response.customerId)
    assert saved_customer.newsletterSubscribed is True


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize("field_name", ["firstName", "lastName"])
@pytest.mark.parametrize("valid_value", CustomerTestData.VALID_NAMES)
def test_register_valid_name_fields(
    field_name, valid_value, cleanup_customer, customers_client
):
    customer = CustomerFactory().create_required_api()

    setattr(customer, field_name, valid_value)
    customer_response = customers_client.create_customer(customer)
    cleanup_customer(customer_response.customerId)

    saved_customer = customers_client.get_customer(customer_response.customerId)

    assert getattr(saved_customer, field_name) == getattr(customer, field_name)


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize("field_name", ["firstName", "lastName"])
@pytest.mark.parametrize("invalid_value", CustomerTestData.INVALID_NAMES)
def test_register_invalid_name_fields(
    field_name, invalid_value, cleanup_customer, customers_client
):
    customer = CustomerFactory().create_required_api()

    setattr(customer, field_name, invalid_value)

    with pytest.raises(HTTPError) as exc_info:
        customer_response = customers_client.create_customer(customer)
        cleanup_customer(customer_response.customerId)

    assert exc_info.value.response is not None
    assert exc_info.value.response.status_code == 422


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize("valid_value", CustomerTestData.VALID_EMAILS)
def test_register_valid_email_field(valid_value, cleanup_customer, customers_client):
    customer = CustomerFactory().create_required_api()
    customer.email = valid_value

    customer_response = customers_client.create_customer(customer)
    cleanup_customer(customer_response.customerId)

    saved_customer = customers_client.get_customer(customer_response.customerId)
    assert saved_customer.email == customer.email


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize("invalid_value", CustomerTestData.INVALID_EMAILS)
def test_register_invalid_email_field(
    invalid_value, cleanup_customer, customers_client
):
    customer = CustomerFactory().create_required_api()
    customer.email = invalid_value

    with pytest.raises(HTTPError) as exc_info:
        customer_response = customers_client.create_customer(customer)
        cleanup_customer(customer_response.customerId)

    assert exc_info.value.response is not None
    assert exc_info.value.response.status_code == 422


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize("valid_value", CustomerTestData.VALID_PASSWORDS)
def test_register_valid_password_field(valid_value, cleanup_customer, customers_client):
    customer = CustomerFactory().create_required_api()
    customer.password = valid_value

    customer_response = customers_client.create_customer(customer)
    cleanup_customer(customer_response.customerId)

    saved_customer = customers_client.get_customer(customer_response.customerId)
    assert saved_customer.email == customer.email


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize("invalid_value", CustomerTestData.INVALID_PASSWORDS)
def test_register_invalid_password_field(
    invalid_value, cleanup_customer, customers_client
):
    customer = CustomerFactory().create_required_api()
    customer.password = invalid_value

    with pytest.raises(HTTPError) as exc_info:
        customer_response = customers_client.create_customer(customer)
        cleanup_customer(customer_response.customerId)

    assert exc_info.value.response is not None
    assert exc_info.value.response.status_code == 422


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize("groups,default_group", CustomerTestData.VALID_GROUPS)
def test_register_valid_groups(
    groups, default_group, cleanup_customer, customers_client
):
    customer = CustomerFactory().create_required_api()
    customer.groupIds = groups
    customer.defaultGroupId = default_group

    customer_response = customers_client.create_customer(customer)
    cleanup_customer(customer_response.customerId)

    saved_customer = customers_client.get_customer(customer_response.customerId)

    assert set(customer.groupIds) == set(saved_customer.groupIds)


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize("groups,default_group", CustomerTestData.INVALID_GROUPS)
def test_register_invalid_groups(
    groups, default_group, cleanup_customer, customers_client
):
    customer = CustomerFactory().create_required_api()
    customer.groupIds = groups
    customer.defaultGroupId = default_group

    with pytest.raises(HTTPError) as exc_info:
        customer_response = customers_client.create_customer(customer)
        cleanup_customer(customer_response.customerId)

    assert exc_info.value.response is not None
    assert exc_info.value.response.status_code in (400, 422)
