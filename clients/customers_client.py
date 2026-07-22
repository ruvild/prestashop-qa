from clients.base_client import BaseClient
from schemas.customer_schemas import CustomerSearchResponse
import json
from schemas.customer_schemas import CustomerCreateRequest, CustomerCreateResponse
from requests import Response
from config.exceptions import CustomerNotFoundError


class CustomersClient(BaseClient):

    def __init__(self) -> None:
        super().__init__()
        self.endpoint = "customers"

    def get_by_email(self, email: str) -> CustomerSearchResponse:
        url = self.build_url(f"{self.endpoint}/search")
        params = {"phrases[]": email}

        res = self.session.get(url, headers=self.auth_header, params=params)
        res.raise_for_status()
        data = res.json()

        if not data:
            raise CustomerNotFoundError(f"No customer found with email: {email}")

        customer_data = next(iter(data.values()))
        print(
            f"{'-'*10}Returned customer{'-'*10}\n{json.dumps(customer_data, indent=4)}\n{'-'*20}"
        )
        return CustomerSearchResponse.model_validate(customer_data)

    def create_customer(
        self, customer: CustomerCreateRequest
    ) -> CustomerCreateResponse:
        url = self.build_url(self.endpoint)
        payload = customer.model_dump(exclude_none=True)
        res = self.session.post(url, headers=self.auth_header, json=payload)
        res.raise_for_status()
        customer_data = res.json()
        print(
            f"{'-'*10}Posted customer{'-'*10}\n{json.dumps(customer_data, indent=4)}\n{'-'*20}"
        )
        return CustomerCreateResponse.model_validate(customer_data)

    def delete_customer(self, customer_id) -> Response:
        url = self.build_url(f"{self.endpoint}/{customer_id}")
        res = self.session.delete(
            url,
            headers=self.auth_header,
            json={"deleteMethod": "allow_registration_after"},
        )
        res.raise_for_status()
        return res
