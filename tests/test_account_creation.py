from playwright.sync_api import expect
from pages.registration_page import BasePage
from pages.registration_page import RegistrationPage
from factories.customer_factory import CustomerFactory
import pytest
from requests import HTTPError
from tests.customer_test_data import CustomerTestData


def test_register_required_ui(page, cleanup_customer, customers_client):
    customer = CustomerFactory.create_required_ui()

    current_page = (
        BasePage(page)
        .navigate()
        .go_to_login_page()
        .create_account()
        .register_valid(customer)
    )

    expect(page).to_have_url(current_page.url)
    expect(current_page.account_header).to_be_visible()

    saved_customer = customers_client.search_customer(customer.email)
    cleanup_customer(saved_customer.idCustomer)

    assert saved_customer.firstname == customer.first_name


def test_register_empty_ui(page):
    current_page = RegistrationPage(page).navigate().register_empty()
    expect(page).to_have_url(current_page.url)
    expect(current_page.email).to_be_visible()


def test_register_optionals_ui(page, cleanup_customer, customers_client):
    customer = CustomerFactory.create_full_ui()

    current_page = (
        RegistrationPage(page).navigate().register_valid(customer, optionals=True)
    )

    expect(page).to_have_url(current_page.url)
    expect(current_page.account_header).to_be_visible()

    saved_customer = customers_client.search_customer(customer.email)
    cleanup_customer(saved_customer.idCustomer)

    assert saved_customer.firstname == customer.first_name


def test_register_required_api(cleanup_customer, customers_client):
    customer = CustomerFactory().create_required_api()

    customer_response = customers_client.create_customer(customer)
    cleanup_customer(customer_response.customerId)

    saved_customer = customers_client.search_customer(customer_response.customerId)
    assert saved_customer.firstname == customer.firstName

    response_dict = customer_response.model_dump()
    assert "password" not in response_dict


def test_register_full_api(customers_client, cleanup_customer):
    customer = CustomerFactory().create_full_api()

    customer_response = customers_client.create_customer(customer)
    cleanup_customer(customer_response.customerId)

    saved_customer = customers_client.search_customer(customer_response.customerId)
    assert saved_customer.firstname == customer.firstName

    response_dict = customer_response.model_dump()
    assert "password" not in response_dict


@pytest.mark.parametrize("field_name", ["firstName", "lastName"])
@pytest.mark.parametrize("valid_value", CustomerTestData.VALID_NAMES)
def test_register_valid_name_fields(
    field_name, valid_value, cleanup_customer, customers_client
):
    customer = CustomerFactory().create_required_api()

    setattr(customer, field_name, valid_value)
    customer_response = customers_client.create_customer(customer)
    cleanup_customer(customer_response.customerId)

    saved_customer = customers_client.search_customer(customer_response.customerId)

    returned_field_name = field_name.lower()
    assert getattr(saved_customer, returned_field_name) == getattr(customer, field_name)


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
    print(exc_info)

    assert "Unprocessable Content" in str(exc_info.value)


@pytest.mark.parametrize("valid_value", CustomerTestData.VALID_EMAILS)
def test_register_valid_email_field(valid_value, cleanup_customer, customers_client):
    customer = CustomerFactory().create_required_api()
    customer.email = valid_value

    customer_response = customers_client.create_customer(customer)
    cleanup_customer(customer_response.customerId)

    saved_customer = customers_client.search_customer(customer_response.customerId)
    assert saved_customer.email == customer.email


@pytest.mark.parametrize("invalid_value", CustomerTestData.INVALID_EMAILS)
def test_register_invalid_email_field(
    invalid_value, cleanup_customer, customers_client
):
    customer = CustomerFactory().create_required_api()
    customer.email = invalid_value

    with pytest.raises(HTTPError) as exc_info:
        customer_response = customers_client.create_customer(customer)
        cleanup_customer(customer_response.customerId)
    print(exc_info)

    assert "Unprocessable Content" in str(exc_info.value)


@pytest.mark.parametrize("valid_value", CustomerTestData.VALID_PASSWORDS)
def test_register_valid_password_field(valid_value, cleanup_customer, customers_client):
    customer = CustomerFactory().create_required_api()
    customer.password = valid_value

    customer_response = customers_client.create_customer(customer)
    cleanup_customer(customer_response.customerId)

    saved_customer = customers_client.search_customer(customer_response.customerId)
    assert saved_customer.email == customer.email


@pytest.mark.parametrize("invalid_value", CustomerTestData.INVALID_PASSWORDS)
def test_register_invalid_password_field(
    invalid_value, cleanup_customer, customers_client
):
    customer = CustomerFactory().create_required_api()
    customer.password = invalid_value

    with pytest.raises(HTTPError) as exc_info:
        customer_response = customers_client.create_customer(customer)
        cleanup_customer(customer_response.customerId)
    print(exc_info)

    assert "Unprocessable Content" in str(exc_info.value)


@pytest.mark.parametrize("groups,default_group", CustomerTestData.VALID_GROUPS)
def test_register_valid_groups(
    groups, default_group, cleanup_customer, customers_client
):
    customer = CustomerFactory().create_required_api()
    customer.groupIds = groups
    customer.defaultGroupId = default_group

    customer_response = customers_client.create_customer(customer)
    cleanup_customer(customer_response.customerId)

    saved_customer = customers_client.search_customer(customer_response.customerId)

    expected_groups = set(customer.groupIds)
    actual_groups = {int(k) for k in saved_customer.groups.keys()}
    assert expected_groups == actual_groups


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
    print(exc_info)

    assert ("Unprocessable Content" in str(exc_info.value)) or (
        "Bad Request" in str(exc_info.value)
    )
