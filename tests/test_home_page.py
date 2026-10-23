from pages.home_page import HomePage
from playwright.sync_api import expect
from config.utils import extract_product_ids
from config.utils import binshops_extractor


def test_category_top_menu_ui(page):
    current_page = HomePage(page).navigate().expand_category_top_menu()
    expect(current_page.category_sublink).to_be_visible()


def test_search_bar_ui(page, product_search_client):

    search_keyword = "hummingbird"
    current_page = HomePage(page).navigate().search_product(search_keyword)
    expect(current_page.search_results_list).to_be_visible()

    product_id_list_ui = [
        option.get_attribute("id") for option in current_page.searched_products.all()
    ]
    res = product_search_client.search_products(query=search_keyword)

    product_id_list_api = binshops_extractor("id_product", res)

    assert set(extract_product_ids(product_id_list_ui)) <= set(product_id_list_api)


def test_main_elements_ui(page):
    current_page = HomePage(page).navigate()

    expect(current_page.carousel).to_be_visible()
    expect(current_page.featured_products_block).to_be_visible()
    expect(current_page.special_deals_block).to_be_visible()


def test_footer_ui(page):
    current_page = HomePage(page).navigate()

    expect(current_page.product_footer).to_be_visible()
    expect(current_page.company_footer).to_be_visible()
    expect(current_page.account_footer).to_be_visible()
    expect(current_page.store_info_footer).to_be_visible()

    login_page = current_page.go_to_login_page_via_footer()
    expect(login_page.email).to_be_visible()
    expect(login_page.password).to_be_visible()
