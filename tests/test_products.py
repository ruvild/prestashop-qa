from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.category_page import CategoryPage
from playwright.sync_api import expect
from test_data.category_test_data import HOME_ACCESSORIES
from clients.binshops.category_products_client import CategoryProductsClient


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


def test_category_page_navigation(page):
    current_page = BasePage(page).navigate().navigate_to_category_page()
    expect(current_page.filter_block).to_be_visible()
    expect(current_page.product_section).to_be_visible()


def test_filters_ui(page, subcategory=HOME_ACCESSORIES):

    BasePage(page).navigate().navigate_to_category_page(subcategory=subcategory)

    filtered_products_ids_ui = CategoryPage(page).get_filtered_products_ids()

    filtered_products_ids_api = CategoryProductsClient().search_category_products(
        subcategory
    )

    assert filtered_products_ids_ui == filtered_products_ids_api


def test_filters_api(products_client, subcategory=HOME_ACCESSORIES):

    id_set_bin = CategoryProductsClient().search_category_products(subcategory)
    id_set_prest = products_client.filter_products_by_category(subcategory)
    assert id_set_bin == id_set_prest
