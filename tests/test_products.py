from pages.base_page import BasePage
from pages.home_page import HomePage
from playwright.sync_api import expect


def test_product_navigation(page):

    current_page = HomePage(page).navigate()
    product = current_page.get_featured_product()
    product_name = product.get_by_label("View product").inner_text()
    product_page = current_page.navigate_to_product_page(product)

    expect(product_page.product_title).to_have_text(product_name)


def test_product_quick_view(page):

    current_page = HomePage(page).navigate()
    quick_view_dialog = current_page.open_quick_view()
    product_name = current_page.quick_view_product_title.inner_text()

    expect(quick_view_dialog.get_by_role("button", name="Add to cart")).to_be_visible()
    product_page = current_page.navigate_to_product_page_via_quick_view()

    expect(product_page.product_title).to_have_text(product_name)
    expect(product_page.add_to_cart_button).to_be_visible()


def test_new_product(page, default_product, products_client):

    new_product_id = default_product.productId
    current_page = HomePage(page).navigate()
    new_product_banner = current_page.get_product_from_new_arrivals(new_product_id)
    expect(new_product_banner).to_be_visible()

    products_client.delete_product(new_product_id)
    page.reload()
    expect(new_product_banner).not_to_be_visible()


def test_category_page(page):
    current_page = BasePage(page).navigate().navigate_to_category_page()
    expect(current_page.filter_block).to_be_visible()
    expect(current_page.product_section).to_be_visible()
