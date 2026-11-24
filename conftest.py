import os
from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Page, Playwright

from clients.admin_api.customers_client import CustomersClient
from clients.admin_api.products_client import ProductsClient
from clients.binshops.auth_client import AuthClient
from clients.binshops.cart_client import CartClient
from clients.binshops.category_products_client import CategoryProductsClient
from clients.binshops.product_search_client import ProductSearchClient
from scripts.setup_api_client import ApiClientSetup
from scripts.setup_environment import ensure_environment


def pytest_configure(config: pytest.Config) -> None:
    if hasattr(config, "workerinput"):
        return

    if os.getenv("CI"):
        ensure_environment()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {**browser_context_args, "reduced_motion": "reduce"}


@pytest.fixture(scope="session")
def auth_key(worker_id: str) -> Generator[str]:

    provisioner = ApiClientSetup(worker_id)
    token = provisioner.setup()

    yield token

    provisioner.teardown()


@pytest.fixture
def customers_client(auth_key: str) -> CustomersClient:
    return CustomersClient(auth_key)


@pytest.fixture
def products_client(auth_key: str) -> ProductsClient:
    return ProductsClient(auth_key)


@pytest.fixture
def auth_client() -> AuthClient:
    return AuthClient()


@pytest.fixture
def browser_auth_client(page: Page) -> AuthClient:
    return AuthClient(page.request)


@pytest.fixture
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext]:
    context = playwright.request.new_context()
    yield context
    context.dispose()


@pytest.fixture
def api_auth_client(api_request_context: APIRequestContext) -> AuthClient:
    return AuthClient(api_request_context)


@pytest.fixture
def api_cart_client(api_request_context: APIRequestContext) -> CartClient:
    return CartClient(api_request_context)


@pytest.fixture
def product_search_client() -> ProductSearchClient:
    return ProductSearchClient()


@pytest.fixture
def category_products_client() -> CategoryProductsClient:
    return CategoryProductsClient()


@pytest.fixture
def cart_client(page: Page) -> CartClient:
    return CartClient(page.request)
