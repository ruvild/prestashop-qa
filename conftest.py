import pytest
from collections.abc import Generator
from scripts.setup_api_client import ApiClientSetup
from scripts.setup_environment import ensure_environment
from clients.admin_api.customers_client import CustomersClient
from clients.admin_api.products_client import ProductsClient
import os


def pytest_configure(config) -> None:
    if hasattr(config, "workerinput"):
        return

    if os.getenv("CI"):
        ensure_environment()


@pytest.fixture(scope="session")
def auth_key(worker_id: str) -> Generator[str, None, None]:

    provisioner = ApiClientSetup(worker_id)
    token = provisioner.setup()

    yield token

    provisioner.teardown()


@pytest.fixture()
def customers_client(auth_key):
    return CustomersClient(auth_key)


@pytest.fixture()
def products_client(auth_key):
    return ProductsClient(auth_key)
