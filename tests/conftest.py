import pytest
from typing import Any
from clients.binshops.base_client import BaseClient
from collections.abc import Generator, Callable
from factories.customer_factory import CustomerFactory
from schemas.customer_schemas import CustomerCreateRequest
from factories.product_factory import ProductFactory
from schemas.product_schemas import ProductResponse
from playwright.sync_api import APIResponse


@pytest.fixture()
def cleanup_customer(customers_client) -> Generator[Callable[[int], None], None, None]:
    created_ids = []

    def add_id(customer_id: int) -> None:
        created_ids.append(customer_id)

    yield add_id

    for customer_id in created_ids:
        _delete_customer(customers_client, customer_id)


@pytest.fixture()
def default_customer(customers_client) -> Generator[CustomerCreateRequest, None, None]:
    customer = CustomerFactory().create_required_api()
    response = customers_client.create_customer(customer)

    yield customer

    _delete_customer(customers_client, response.customerId)


def _delete_customer(customers_client, customer_id: int) -> None:
    try:
        customers_client.delete_customer(customer_id)
    except Exception as e:
        print(f"\n[Teardown Warning] Failed to delete customer {customer_id}: {e}")


@pytest.fixture
def default_product(products_client) -> Generator[ProductResponse, None, None]:
    client = products_client
    product = ProductFactory().create_base_product()
    response = client.create_product(product)
    product_id = response.productId

    try:
        baseline_patch_data = {
            "enabled": True,
            "descriptions": {
                "en-US": "This is a beautiful mug for testing. Perfect for a well-deserved break."
            },
            "shortDescriptions": {"en-US": "This is a mug."},
            "priceTaxExcluded": 10.0,
            "reference": "test_mug",
        }

        patch_response = client.update_product(product_id, baseline_patch_data)

        yield patch_response

    finally:
        try:
            client.delete_product(product_id)
        except Exception as e:
            print(f"\n[Teardown Warning] Failed to delete product {product_id}: {e}")


@pytest.fixture
def get_order_info(page) -> Callable[[int], dict[str, Any]]:

    def _make_request(order_id: int) -> dict[str, Any]:
        url = BaseClient().build_url(f"orderhistory?id_order={order_id}")
        response = page.request.get(url)
        assert (
            response.ok
        ), f"Failed to fetch order info: {response.status} {response.text()}"
        return response.json()

    return _make_request


@pytest.fixture
def get_account_info(page) -> Callable[[], dict[str, Any]]:
    def _make_request() -> dict[str, Any]:
        url = BaseClient().build_url("accountInfo")
        response = page.request.get(url)

        assert (
            response.ok
        ), f"Failed to fetch account info: {response.status} {response.text()}"
        return response.json()

    return _make_request


@pytest.fixture
def login_user(page) -> Callable[[str, str], APIResponse]:
    def _login(email: str, password: str) -> APIResponse:
        response = page.request.post(
            f"{BaseClient().build_url('login')}",
            data={"email": email, "password": password},
        )
        assert response.ok, f"Login failed: {response.status} {response.text()}"
        return response

    return _login
