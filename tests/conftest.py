import pytest
from collections.abc import Iterator


@pytest.fixture
def cleanup_customer(customers_client) -> Iterator[dict[str, str]]:
    context = {"email": ""}
    yield context

    email = context["email"]
    if email:
        try:
            customer = customers_client.get_by_email(email)
            if customer:
                customers_client.delete_customer(customer.idCustomer)
        except Exception as e:
            print(f"\n[Teardown Warning] Failed to auto-delete customer '{email}': {e}")
