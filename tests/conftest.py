import pytest
from collections.abc import Iterator
from clients.customers_client import CustomersClient


@pytest.fixture
def cleanup_customer() -> Iterator[dict[str, str]]:
    context = {"email": ""}
    yield context

    email = context["email"]
    if email:
        client = CustomersClient()
        try:
            customer = client.get_by_email(email)
            if customer:
                client.delete_customer(customer.idCustomer)
        except Exception as e:
            print(f"\n[Teardown Warning] Failed to auto-delete customer '{email}': {e}")
