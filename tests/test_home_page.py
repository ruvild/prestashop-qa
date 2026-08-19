from pages.base_page import BasePage
from playwright.sync_api import expect
from config.utils import extract_product_ids


def test_category_top_menu_ui(page):
    current_page = BasePage(page).navigate().expand_category_top_menu()
    expect(current_page.category_sublink).to_be_visible()


def test_search_bar_ui(page):
    search_keyword = "mug"
    current_page = BasePage(page).navigate().search_product(search_keyword)
    expect(current_page.search_results_list).to_be_visible()

    product_id_list_ui = [
        option.get_attribute("id") for option in current_page.searched_products.all()
    ]
    res = page.request.get(
        f"{current_page.base_url}rest/productSearch?s={search_keyword}"
    )
    product_id_list_api = {
        product["id_product"] for product in res.json()["psdata"]["products"]
    }

    assert set(extract_product_ids(product_id_list_ui)) <= product_id_list_api
