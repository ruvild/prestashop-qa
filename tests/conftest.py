import logging
from collections.abc import Callable, Generator

import pytest
from playwright.sync_api import Page

from clients.admin_api.customers_client import CustomersClient
from clients.admin_api.products_client import ProductsClient
from clients.binshops.base_client import BaseClient
from factories.customer_factory import CustomerFactory
from factories.product_factory import ProductFactory
from schemas.customer_schemas import CustomerCreateRequest
from schemas.order_schemas import OrderResponse
from schemas.product_schemas import ProductResponse

logger = logging.getLogger(__name__)


@pytest.fixture
def cleanup_customer(
    customers_client: CustomersClient,
) -> Generator[Callable[[int], None]]:
    created_ids: list[int] = []

    def add_id(customer_id: int) -> None:
        created_ids.append(customer_id)

    yield add_id

    for customer_id in created_ids:
        _delete_customer(customers_client, customer_id)


@pytest.fixture
def default_customer(
    customers_client: CustomersClient,
) -> Generator[CustomerCreateRequest]:
    customer = CustomerFactory.create_required_api()
    response = customers_client.create_customer(customer)

    yield customer

    _delete_customer(customers_client, response.customerId)


def _delete_customer(customers_client: CustomersClient, customer_id: int) -> None:
    try:
        customers_client.delete_customer(customer_id)
    except Exception as e:
        logger.warning(
            "[Teardown Warning] Failed to delete customer %s: %s", customer_id, e
        )


@pytest.fixture
def default_product(
    products_client: ProductsClient,
) -> Generator[ProductResponse]:
    product = ProductFactory().create_base_product()
    response = products_client.create_product(product)
    product_id = response.productId

    try:
        baseline_patch_data = {
            "enabled": True,
            "descriptions": {
                "en-US": "This is a beautiful mug for testing. Perfect for a well-deserved break."
            },
            "shortDescriptions": {"en-US": "This is a mug."},
            "priceTaxExcluded": 10.0,
            "reference": f"test_mug_{product_id}",
        }

        patch_response = products_client.update_product(product_id, baseline_patch_data)

        yield patch_response

    finally:
        try:
            products_client.delete_product(product_id)
        except Exception as e:
            logger.warning(
                "[Teardown Warning] Failed to delete product %s: %s", product_id, e
            )


@pytest.fixture
def get_order_info(page: Page) -> Callable[[int], OrderResponse]:

    def _make_request(order_id: int) -> OrderResponse:
        url = BaseClient(create_session=False).build_url(
            f"orderhistory?id_order={order_id}"
        )
        response = page.request.get(url, timeout=30_000)
        assert (
            response.ok
        ), f"Failed to fetch order info: {response.status} {response.text()}"
        return OrderResponse.model_validate(response.json())

    return _make_request
