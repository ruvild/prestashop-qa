import re

import pytest
from playwright.sync_api import expect

from config.utils import get_order_id_from_url, stock_changer
from pages.cart_page import CartPage
from pages.home_page import HomePage
from schemas.cart_schemas import ProductToCart
from test_data.customer_test_data import (
    DEFAULT_ADDRESS_DATA,
    INVALID_POSTCODE_ADDRESS_DATA,
)
from test_data.product_test_data import ADD_PRODUCT_TO_CART, ProductTestData


@pytest.mark.smoke
@pytest.mark.hybrid
def test_cart_behavior(page, cart_client):
    home_page = HomePage(page).navigate()
    product = home_page.get_featured_product()

    product_id = product.get_attribute("data-id-product")
    product_attribute_id = product.get_attribute("data-id-product-attribute")

    assert product_id is not None, "Product ID attribute is missing"
    assert product_attribute_id is not None, "Product attribute ID is missing"

    product_id = int(product_id)
    product_attribute_id = int(product_attribute_id)

    product_quantity = product.locator('input[name="qty"]').input_value()

    added_to_cart_popup = home_page.add_product_to_cart(product)
    expect(added_to_cart_popup).to_be_visible()

    cart_page = home_page.proceed_to_checkout()

    product_block = cart_page.get_product(product_id, product_attribute_id)
    expect(product_block).to_have_count(1)

    cart_quantity = product_block.locator(
        'input[name="product-quantity-spin"]'
    ).input_value()

    assert int(product_quantity) == int(cart_quantity)

    cart_res = cart_client.get_cart_contents()
    api_products = cart_res.psdata.products

    matching_products = [
        item
        for item in api_products
        if item.id_product == product_id
        and item.id_product_attribute == product_attribute_id
    ]

    assert len(matching_products) == 1, (
        f"Expected exactly one matching cart item for product {product_id}, "
        f"attribute {product_attribute_id}; found {len(matching_products)}"
    )

    assert matching_products[0].cart_quantity == int(cart_quantity)


@pytest.mark.regression
@pytest.mark.hybrid
def test_cart_quantity_update(page, default_customer, browser_auth_client, cart_client):
    login_res = browser_auth_client.login(
        email=default_customer.email, password=default_customer.password
    )
    assert login_res.success is True

    cart_res = cart_client.add_product_to_cart(ADD_PRODUCT_TO_CART)
    assert cart_res.success is True

    product_id = ADD_PRODUCT_TO_CART.id_product
    product_attribute_id = ADD_PRODUCT_TO_CART.id_product_attribute
    assert product_attribute_id is not None

    cart_page = CartPage(page).navigate()
    qty_input = cart_page.get_quantity_input(product_id, product_attribute_id)
    expect(qty_input).to_have_value(str(ADD_PRODUCT_TO_CART.qty))

    increased_qty = ADD_PRODUCT_TO_CART.qty + 1
    cart_page.increase_product_quantity(product_id, product_attribute_id)
    expect(qty_input).to_have_value(str(increased_qty))
    expect(cart_page.cart_summary).to_contain_text(f"{increased_qty} items")

    updated_cart = cart_client.get_cart_contents()
    assert updated_cart.psdata.products[0].cart_quantity == increased_qty

    cart_page.decrease_product_quantity(product_id, product_attribute_id)
    expect(qty_input).to_have_value(str(ADD_PRODUCT_TO_CART.qty))
    expect(cart_page.cart_summary).to_contain_text(f"{ADD_PRODUCT_TO_CART.qty} items")

    reverted_cart = cart_client.get_cart_contents()
    assert reverted_cart.psdata.products[0].cart_quantity == ADD_PRODUCT_TO_CART.qty


@pytest.mark.regression
@pytest.mark.hybrid
def test_remove_cart_item(page, default_customer, browser_auth_client, cart_client):
    login_res = browser_auth_client.login(
        email=default_customer.email, password=default_customer.password
    )
    assert login_res.success is True

    cart_res = cart_client.add_product_to_cart(ADD_PRODUCT_TO_CART)
    assert cart_res.success is True

    product_id = ADD_PRODUCT_TO_CART.id_product
    product_attribute_id = ADD_PRODUCT_TO_CART.id_product_attribute
    assert product_attribute_id is not None

    cart_page = CartPage(page).navigate()
    cart_page.remove_product(product_id, product_attribute_id)

    expect(cart_page.get_product(product_id, product_attribute_id)).to_have_count(0)
    expect(cart_page.empty_cart_message).to_be_visible()

    updated_cart = cart_client.get_cart_contents()
    assert updated_cart.psdata.products == []


@pytest.mark.smoke
@pytest.mark.hybrid
def test_full_checkout(
    page,
    default_customer,
    cart_client,
    get_order_info,
    customers_client,
    browser_auth_client,
):
    cart_page = CartPage(page)

    login_res = browser_auth_client.login(
        email=default_customer.email, password=default_customer.password
    )
    assert login_res.success is True

    cart_res = cart_client.add_product_to_cart(ADD_PRODUCT_TO_CART)
    assert cart_res.success

    cart_product = cart_res.psdata.products[0]

    assert cart_product.id_product == ADD_PRODUCT_TO_CART.id_product
    assert cart_product.id_product_attribute == ADD_PRODUCT_TO_CART.id_product_attribute
    assert cart_product.cart_quantity == ADD_PRODUCT_TO_CART.qty

    order_page = (
        cart_page.navigate().proceed_to_checkout().insert_address(DEFAULT_ADDRESS_DATA)
    )

    expect(order_page.default_delivery_option).to_be_checked()

    confirmation_page = order_page.proceed_to_payment().place_order()

    expect(confirmation_page.order_confirmed_block).to_contain_text(
        "Your order is confirmed"
    )
    expect(confirmation_page.order_details_block).to_be_visible()

    order_id = get_order_id_from_url(page.url)
    order_res = get_order_info(order_id)
    order_data = order_res.psdata

    assert order_data.details.id == order_id

    products = order_data.products
    assert len(products) == 1, f"Expected one product, got {len(products)}"

    order_product = next(iter(products.values()))

    assert order_product.id_product == cart_product.id_product
    assert order_product.product_attribute_id == cart_product.id_product_attribute
    assert order_product.quantity == cart_product.cart_quantity

    customer_data = customers_client.search_customer_by_email(default_customer.email)
    assert order_data.addresses.delivery.id_customer == customer_data.idCustomer

    order_details = order_data.details
    shipping_details = order_details.shipping[0]

    assert order_details.reference in confirmation_page.order_reference.inner_text()
    assert order_details.payment in confirmation_page.payment_method.inner_text()
    assert (
        shipping_details.carrier_name in confirmation_page.shipping_method.inner_text()
    )
    assert order_product.product_name in confirmation_page.product_title.inner_text()

    assert str(order_product.quantity) == re.sub(
        r"\D", "", confirmation_page.quantity.inner_text()
    )
    assert (
        order_data.totals.total_including_tax.value
        == confirmation_page.total_value.inner_text()
    )


@pytest.mark.regression
@pytest.mark.ui
def test_checkout_invalid_postcode_ui(
    page, default_customer, browser_auth_client, cart_client
):
    login_res = browser_auth_client.login(
        email=default_customer.email, password=default_customer.password
    )
    assert login_res.success is True

    cart_res = cart_client.add_product_to_cart(ADD_PRODUCT_TO_CART)
    assert cart_res.success is True

    order_page = (
        CartPage(page)
        .navigate()
        .proceed_to_checkout()
        .insert_address(INVALID_POSTCODE_ADDRESS_DATA)
    )

    expect(page).to_have_url(re.compile(rf"^{re.escape(order_page.url)}"))
    expect(order_page.address_error_alert).to_be_visible()
    expect(order_page.address_error_alert).to_contain_text("Invalid postcode")
    expect(order_page.default_delivery_option).to_be_hidden()


@pytest.mark.regression
@pytest.mark.ui
def test_checkout_empty_address_ui(
    page, default_customer, browser_auth_client, cart_client
):
    login_res = browser_auth_client.login(
        email=default_customer.email, password=default_customer.password
    )
    assert login_res.success is True

    cart_res = cart_client.add_product_to_cart(ADD_PRODUCT_TO_CART)
    assert cart_res.success is True

    order_page = CartPage(page).navigate().proceed_to_checkout()
    order_page.go_to_shipping_button.click()

    expect(page).to_have_url(order_page.url)
    assert order_page.address.evaluate("el => el.validity.valueMissing") is True
    expect(order_page.default_delivery_option).to_be_hidden()


@pytest.mark.regression
@pytest.mark.ui
def test_checkout_unchecked_tos_ui(
    page, default_customer, browser_auth_client, cart_client
):
    login_res = browser_auth_client.login(
        email=default_customer.email, password=default_customer.password
    )
    assert login_res.success is True

    cart_res = cart_client.add_product_to_cart(ADD_PRODUCT_TO_CART)
    assert cart_res.success is True

    order_page = (
        CartPage(page)
        .navigate()
        .proceed_to_checkout()
        .insert_address(DEFAULT_ADDRESS_DATA)
        .proceed_to_payment()
    )
    order_page.wire_payment_option.check()

    expect(order_page.tos_agreement).not_to_be_checked()
    expect(order_page.place_order_button).to_be_disabled()
    expect(page).to_have_url(order_page.url)


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize(
    "stock_quantity, requested_quantity, expected_error",
    ProductTestData.PRODUCT_STOCK,
)
def test_stock(
    api_auth_client,
    default_customer,
    default_product,
    api_cart_client,
    stock_quantity,
    requested_quantity,
    expected_error,
):
    login_res = api_auth_client.login(
        email=default_customer.email, password=default_customer.password
    )
    assert login_res.success is True
    product_id = default_product.productId
    stock_changer(product_id, stock_quantity)

    added_product = ProductToCart(
        id_product=product_id, op="up", qty=requested_quantity
    )
    cart_res = api_cart_client.add_product_to_cart(added_product)

    errors = cart_res.psdata.errors
    if not expected_error:
        assert not errors
    else:
        assert len(errors) == 1
        assert expected_error in errors[0].lower()
