from clients.admin_api.base_client import BaseClient
from schemas.customer_schemas import CustomerSearchResponse
from schemas.customer_schemas import CustomerCreateRequest, CustomerCreateResponse
from requests import Response
from config.exceptions import CustomerNotFoundError


class CustomersClient(BaseClient):

    def __init__(self, auth_token) -> None:
        super().__init__(auth_token)
        self.endpoint = "customers"

    def search_customer(self, query: int | str) -> CustomerSearchResponse:
        url = self.build_url(f"{self.endpoint}/search")
        params = {"phrases[]": query}

        res = self.session.get(url, headers=self.auth_header, params=params)
        res.raise_for_status()
        data = res.json()

        if not data:
            raise CustomerNotFoundError(f"No customer found by searching <{query}>")

        customer_data = next(iter(data.values()))
        print(
            f"Customer with id <{customer_data.get('idCustomer')}> found, email: {customer_data.get('email')}"
        )
        return CustomerSearchResponse.model_validate(customer_data)

    def create_customer(
        self, customer: CustomerCreateRequest
    ) -> CustomerCreateResponse:
        url = self.build_url(self.endpoint)
        payload = customer.model_dump(exclude_none=True)
        res = self.session.post(url, headers=self.auth_header, json=payload)
        res.raise_for_status()
        customer_data: dict = res.json()
        print(
            f"Customer {customer_data.get('email')} created with id: {customer_data.get('customerId')}"
        )
        return CustomerCreateResponse.model_validate(customer_data)

    def delete_customer(self, customer_id: int) -> Response:
        url = self.build_url(f"{self.endpoint}/{customer_id}")
        res = self.session.delete(
            url,
            headers=self.auth_header,
            json={"deleteMethod": "allow_registration_after"},
        )
        res.raise_for_status()
        print(f"Customer with id <{customer_id}> deleted")
        return res
