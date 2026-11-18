from pages.login_page import LoginPage
from playwright.sync_api import expect
from test_data.customer_test_data import LoginTestData
import pytest


@pytest.mark.smoke
@pytest.mark.hybrid
def test_valid_login_logout_ui(page, default_customer, get_account_info):
    customer = default_customer
    current_page = LoginPage(page).navigate().sign_in(customer.email, customer.password)

    expect(page).to_have_url(current_page.url)
    expect(current_page.account_header).to_be_visible()

    account = get_account_info()

    assert account["success"] is True
    assert account["psdata"]["logged"] is True
    assert account["psdata"]["email"] == customer.email

    current_page.log_out()
    expect(current_page.sign_in_header).to_be_visible()

    account = get_account_info()
    assert account["success"] is False
    assert "Not Authenticated" in account["message"]


@pytest.mark.regression
@pytest.mark.ui
def test_invalid_password_login_ui(page, default_customer):
    customer = default_customer
    current_page = (
        LoginPage(page)
        .navigate()
        .sign_in_with_invalid_password(customer.email, customer.password)
    )

    expect(page).to_have_url(current_page.url)
    expect(current_page.auth_fail_alert).to_be_visible()


@pytest.mark.smoke
@pytest.mark.api
def test_valid_login_logout_api(auth_client, default_customer):
    customer = default_customer

    login_response = auth_client.login(email=customer.email, password=customer.password)

    assert login_response.success is True
    assert login_response.code == 200
    assert login_response.psdata.status == "success"
    assert login_response.psdata.message == "User login successfully"
    assert login_response.psdata.user.email == customer.email
    assert login_response.psdata.user.logged is True
    assert login_response.psdata.customer_id == login_response.psdata.user.id

    user_fields = login_response.psdata.user.model_dump()
    assert LoginTestData.SENSITIVE_USER_FIELDS.isdisjoint(user_fields.keys())

    account = auth_client.get_account_info()
    assert account.success is True
    assert account.code == 200
    assert account.psdata.logged is True
    assert account.psdata.email == customer.email
    assert LoginTestData.SENSITIVE_USER_FIELDS.isdisjoint(
        account.psdata.model_dump().keys()
    )

    logout_response = auth_client.logout()
    assert logout_response.success is True
    assert logout_response.code == 200

    account_after_logout = auth_client.get_account_info()
    assert account_after_logout.success is False
    assert account_after_logout.code == 410
    assert "Not Authenticated" in account_after_logout.message


@pytest.mark.regression
@pytest.mark.api
def test_login_uppercase_email_api(auth_client, default_customer):
    customer = default_customer

    login_response = auth_client.login(
        email=customer.email.upper(), password=customer.password
    )

    assert login_response.success is True
    assert login_response.code == 200
    assert login_response.psdata.status == "success"
    assert login_response.psdata.user.email == customer.email

    account = auth_client.get_account_info()
    assert account.success is True
    assert account.psdata.logged is True


@pytest.mark.regression
@pytest.mark.api
def test_login_wrong_password_api(auth_client, default_customer):
    customer = default_customer

    login_response = auth_client.login(
        email=customer.email, password=f"{customer.password}_wrong"
    )

    assert login_response.success is True
    assert login_response.code == 306
    assert login_response.psdata == "Authentication failed"

    account = auth_client.get_account_info()
    assert account.success is False
    assert account.code == 410


@pytest.mark.regression
@pytest.mark.api
def test_login_nonexistent_email_api(auth_client):
    login_response = auth_client.login(
        email="nonexistent@example.com", password="ValidPassword1!"
    )

    assert login_response.success is True
    assert login_response.code == 306
    assert login_response.psdata == "Authentication failed"

    account = auth_client.get_account_info()
    assert account.success is False
    assert account.code == 410


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize("payload", LoginTestData.MISSING_EMAIL_PAYLOADS)
def test_login_missing_email_api(auth_client, payload):
    login_response = auth_client.login(payload=payload)

    assert login_response.success is True
    assert login_response.code == 301
    assert login_response.psdata == "An email address required"


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize("invalid_email", LoginTestData.INVALID_EMAILS)
def test_login_invalid_email_api(auth_client, invalid_email):
    login_response = auth_client.login(
        email=invalid_email, password="ValidPassword1!"
    )

    assert login_response.success is True
    assert login_response.code == 302
    assert login_response.psdata == "Invalid email address"


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize("payload", LoginTestData.MISSING_PASSWORD_PAYLOADS)
def test_login_missing_password_api(auth_client, payload):
    login_response = auth_client.login(payload=payload)

    assert login_response.success is True
    assert login_response.code == 303
    assert login_response.psdata == "Password is not provided"


@pytest.mark.regression
@pytest.mark.api
def test_login_disabled_customer_api(auth_client, customers_client, default_customer):
    customer = default_customer
    saved_customer = customers_client.search_customer_by_email(customer.email)
    customers_client.update_customer(saved_customer.idCustomer, {"enabled": False})

    login_response = auth_client.login(email=customer.email, password=customer.password)

    assert login_response.success is True
    assert login_response.code == 305
    assert login_response.psdata == "Your account isn't available at this time."

    account = auth_client.get_account_info()
    assert account.success is False
    assert account.code == 410


@pytest.mark.regression
@pytest.mark.api
def test_login_unsupported_get_method_api(auth_client):
    response = auth_client.send_unsupported_method("GET")

    assert response.success is True
    assert response.code == 310
    assert response.psdata is None
    assert response.message == "GET not supported on this path"
