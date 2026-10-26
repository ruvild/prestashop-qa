from pages.home_page import HomePage
from playwright.sync_api import expect


def test_cart_behavior(page):
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

    response = page.request.get(f"{cart_page.base_url}rest/cart")
    assert response.ok, f"Cart API request failed: {response.status}"

    response_data = response.json()
    api_products = response_data["psdata"]["products"]

    matching_products = [
        item
        for item in api_products
        if item["id_product"] == product_id
        and item["id_product_attribute"] == product_attribute_id
    ]

    assert len(matching_products) == 1, (
        f"Expected exactly one matching cart item for product {product_id}, "
        f"attribute {product_attribute_id}; found {len(matching_products)}"
    )

    assert matching_products[0]["cart_quantity"] == int(cart_quantity)
