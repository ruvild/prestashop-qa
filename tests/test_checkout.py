from pages.home_page import HomePage
from pages.cart_page import CartPage
from playwright.sync_api import expect
from test_data.customer_test_data import DEFAULT_ADDRESS_DATA
from test_data.product_test_data import ADD_PRODUCT_TO_CART
from config.utils import get_order_id_from_url
import re
from schemas.cart_schemas import CartResponse
from schemas.order_schemas import OrderResponse


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

    response_data = cart_client.get_cart_contents()
    cart_res = CartResponse.model_validate(response_data)
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


def test_full_checkout(
    page, default_customer, cart_client, get_order_info, customers_client, login_user
):
    cart_page = CartPage(page)

    login_user(default_customer.email, default_customer.password)

    cart_response = cart_client.add_product_to_cart(ADD_PRODUCT_TO_CART)
    cart_res = CartResponse.model_validate(cart_response)

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
    order_res = OrderResponse.model_validate(get_order_info(order_id))
    order_data = order_res.psdata

    assert order_data.details.id == order_id

    products = order_data.products
    assert len(products) == 1, f"Expected one product, got {len(products)}"

    order_product = next(iter(products.values()))

    assert order_product.id_product == cart_product.id_product
    assert order_product.product_attribute_id == cart_product.id_product_attribute
    assert order_product.quantity == cart_product.cart_quantity

    customer_data = customers_client.search_customer(default_customer.email)
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
