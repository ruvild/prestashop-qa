from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.category_page import CategoryPage
from pages.product_page import ProductPage
from playwright.sync_api import expect
from test_data.product_test_data import HOME_ACCESSORIES
from test_data.product_test_data import ProductTestData
from config.utils import binshops_product_extractor
import pytest
from config.utils import product_url_parser
import re


def test_product_navigation(page, products_client):

    current_page = HomePage(page).navigate()
    product = current_page.get_featured_product()
    product_name = product.get_by_label("View product").inner_text()
    product_page = current_page.navigate_to_product_page(product)

    expect(product_page.product_title).to_have_text(product_name)

    product_url_data = product_url_parser(page.url)
    product_id: int = product_url_data["product_id"]
    product_data = products_client.get_product(product_id)

    assert product_name == product_data["names"]["en-US"]


def test_product_quick_view(page):

    current_page = HomePage(page).navigate()
    quick_view_dialog = current_page.open_quick_view()
    product_name = current_page.quick_view_product_title.inner_text()

    expect(quick_view_dialog.get_by_role("button", name="Add to cart")).to_be_visible()
    product_page = current_page.navigate_to_product_page_via_quick_view()

    expect(product_page.product_title).to_have_text(product_name)
    expect(product_page.add_to_cart_button).to_be_visible()


def test_new_product(page, default_product):

    new_product_id = default_product.productId
    current_page = HomePage(page).navigate()
    new_product_banner = current_page.get_product_from_new_arrivals(new_product_id)
    expect(new_product_banner).to_be_visible()


def test_category_page_navigation(page):
    current_page = BasePage(page).navigate().navigate_to_category_page()
    expect(current_page.filter_block).to_be_visible()
    expect(current_page.product_section).to_be_visible()


def test_filters_ui(page, category_products_client, subcategory=HOME_ACCESSORIES):

    BasePage(page).navigate().navigate_to_category_page(subcategory=subcategory)

    response = category_products_client.search_category_products(subcategory)
    filtered_products_ids_api = set(binshops_product_extractor("id_product", response))

    category_page = CategoryPage(page)
    expect(category_page.filtered_products).to_have_count(
        len(filtered_products_ids_api)
    )

    filtered_products_ids_ui = category_page.get_filtered_products_ids()

    assert filtered_products_ids_ui == filtered_products_ids_api

    assert filtered_products_ids_ui == filtered_products_ids_api


def test_category_filters_api(
    products_client, category_products_client, subcategory=HOME_ACCESSORIES
):

    response = category_products_client.search_category_products(subcategory)
    id_set_bin = set(binshops_product_extractor("id_product", response))
    id_set_prest = products_client.filter_products_by_category(subcategory)
    assert id_set_bin == id_set_prest


@pytest.mark.parametrize(
    "lowest_price,highest_price", ProductTestData.PRODUCT_PRICE_RANGES_EXIST
)
def test_price_filters_match_api(
    lowest_price, highest_price, category_products_client, subcategory=HOME_ACCESSORIES
):

    filters = {"q": f"Price-€-{lowest_price}-{highest_price}"}

    response = category_products_client.search_category_products(
        subcategory, additional_filters=filters
    )
    price_list_raw = binshops_product_extractor("price", response)
    search_list = [float(item[1:]) for item in price_list_raw]

    assert search_list
    assert all(
        lowest_price <= product_price <= highest_price for product_price in search_list
    )


@pytest.mark.parametrize(
    "lowest_price,highest_price", ProductTestData.PRODUCT_PRICE_RANGES_NOT_EXIST
)
def test_price_filters_no_match_api(
    lowest_price, highest_price, category_products_client, subcategory=HOME_ACCESSORIES
):

    filters = {"q": f"Price-€-{lowest_price}-{highest_price}"}

    response = category_products_client.search_category_products(
        subcategory, additional_filters=filters
    )
    price_list_raw = binshops_product_extractor("price", response)
    search_list = [float(item[1:]) for item in price_list_raw]

    assert not search_list


@pytest.mark.parametrize("query", ProductTestData.SEARCH_QUERIES_ERROR)
def test_product_search_error(query, product_search_client):
    response = product_search_client.search_products(query=query)
    assert response["success"] is False


@pytest.mark.parametrize("query", ProductTestData.SEARCH_QUERIES_NO_MATCHES)
def test_product_search_no_matches(query, product_search_client):
    response = product_search_client.search_products(query=query)
    assert not response["psdata"]["products"]


@pytest.mark.xfail(
    reason="Binshops productSearch crashes when a product has no image",
    strict=True,
)
@pytest.mark.parametrize("query", ProductTestData.SEARCH_QUERIES_MATCH_FOUND)
def test_product_search_match_found(query, default_product, product_search_client):
    new_product_id = default_product.productId
    response = product_search_client.search_products(query=query)
    product_ids = binshops_product_extractor("id_product", response)
    assert new_product_id in product_ids


@pytest.mark.parametrize("field, sort_order", ProductTestData.PRODUCT_SORTING_METHODS)
def test_product_sorting(field, sort_order, product_search_client):
    response = product_search_client.search_products(sort_order=sort_order)
    search_list = binshops_product_extractor(field, response)

    if field == "price":
        search_list = [float(item[1:]) for item in search_list]
    elif field == "position":
        search_list = [int(item) for item in search_list]

    if sort_order.endswith(".desc"):
        assert search_list == sorted(search_list, reverse=True)
    else:
        assert search_list == sorted(search_list)


def test_product_color_selection(page, products_client):
    product_page = ProductPage(page)
    page.goto(f"{product_page.base_url}1-1-hummingbird-printed-t-shirt.html")

    product_page.black_color_option.click()
    expect(page).to_have_url(re.compile(r"color-black"))
    expect(product_page.inner_black_color_button).to_be_checked()

    product_url_data = product_url_parser(page.url)

    size_id: str = product_url_data["attributes"]["size"]["attribute_id"]
    size_value: str = product_url_data["attributes"]["size"]["value"]
    color_value: str = product_url_data["attributes"]["color"]["value"]

    expect(product_page.size_dropdown).to_have_value(size_id)

    combination_id: str = product_url_data["combination_id"]
    product_api_data = products_client.search_product_combination(combination_id)

    assert product_url_data["product_id"] == product_api_data["productId"]
    assert product_api_data["combinationId"] == combination_id
    assert (
        product_api_data["name"].lower()
        == f"size - {size_value}, color - {color_value}"
    )


def test_pagination_api(product_search_client):
    results_per_page = 2

    res_page_1 = product_search_client.search_products(
        results_per_page=results_per_page, page=1
    )
    page_1_ids = set(binshops_product_extractor("id_product", res_page_1))

    res_page_2 = product_search_client.search_products(
        results_per_page=results_per_page, page=2
    )
    page_2_ids = set(binshops_product_extractor("id_product", res_page_2))

    assert 0 < len(page_2_ids) <= len(page_1_ids) == results_per_page
    assert page_1_ids.isdisjoint(page_2_ids)
