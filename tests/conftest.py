import pytest
from collections.abc import Generator, Callable
from factories.customer_factory import CustomerFactory
from schemas.customer_schemas import CustomerCreateRequest


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
