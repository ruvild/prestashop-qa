from pages.login_page import LoginPage
from playwright.sync_api import expect


def test_valid_login_logout_ui(page, default_customer):
    customer = default_customer
    current_page = LoginPage(page).navigate().sign_in(customer.email, customer.password)

    expect(page).to_have_url(current_page.url)
    expect(current_page.account_header).to_be_visible()

    response = page.request.get(f"{current_page.base_url}rest/accountInfo")

    expect(response).to_be_ok()
    account = response.json()

    assert account["success"] is True
    assert account["psdata"]["logged"] is True
    assert account["psdata"]["email"] == customer.email

    current_page.log_out()
    expect(current_page.sign_in_header).to_be_visible()

    response = page.request.get(f"{current_page.base_url}rest/accountInfo")
    expect(response).to_be_ok()

    account = response.json()
    assert account["success"] is False
    assert "Not Authenticated" in account["message"]


def test_invalid_password_login_ui(page, default_customer):
    customer = default_customer
    current_page = (
        LoginPage(page)
        .navigate()
        .sign_in_with_invalid_password(customer.email, customer.password)
    )

    expect(page).to_have_url(current_page.url)
    expect(current_page.auth_fail_alert).to_be_visible()
