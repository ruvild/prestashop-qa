import logging

from requests import Response

from clients.admin_api.base_client import BaseClient
from config.exceptions import CustomerNotFoundError
from schemas.customer_schemas import (
    CustomerCreateRequest,
    CustomerCreateResponse,
    CustomerPatchRequest,
    CustomerResponse,
    CustomerSearchResponse,
)

logger = logging.getLogger(__name__)


class CustomersClient(BaseClient):

    def __init__(self, auth_token: str) -> None:
        super().__init__(auth_token)
        self.endpoint = "customers"

    def get_customer(self, customer_id: int) -> CustomerResponse:
        url = self.build_url(f"{self.endpoint}/{customer_id}")
        res = self.session.get(url, headers=self.auth_header, timeout=self.timeout)
        res.raise_for_status()

        return CustomerResponse.model_validate(res.json())

    def search_customer_by_email(self, email: str) -> CustomerSearchResponse:
        url = self.build_url(f"{self.endpoint}/search")
        params = {"phrases[]": email}

        res = self.session.get(
            url, headers=self.auth_header, params=params, timeout=self.timeout
        )
        res.raise_for_status()
        data = res.json()

        if not data:
            raise CustomerNotFoundError(f"No customer found with email <{email}>")

        return CustomerSearchResponse.model_validate(next(iter(data.values())))

    def create_customer(
        self, customer: CustomerCreateRequest
    ) -> CustomerCreateResponse:
        url = self.build_url(self.endpoint)
        payload = customer.model_dump(exclude_none=True)
        res = self.session.post(
            url, headers=self.auth_header, json=payload, timeout=self.timeout
        )
        res.raise_for_status()
        customer_data: dict = res.json()
        logger.info(
            "Customer %s created with id: %s",
            customer_data.get("email"),
            customer_data.get("customerId"),
        )
        return CustomerCreateResponse.model_validate(customer_data)

    def update_customer(self, customer_id: int, patch_data: dict) -> CustomerResponse:
        url = self.build_url(f"{self.endpoint}/{customer_id}")
        validated_patch_data = CustomerPatchRequest.model_validate(patch_data)
        payload: dict = validated_patch_data.model_dump(exclude_none=True)
        res = self.session.patch(
            url, headers=self.auth_header, json=payload, timeout=self.timeout
        )
        res.raise_for_status()
        return CustomerResponse.model_validate(res.json())

    def delete_customer(self, customer_id: int) -> Response:
        url = self.build_url(f"{self.endpoint}/{customer_id}")
        res = self.session.delete(
            url,
            headers=self.auth_header,
            json={"deleteMethod": "allow_registration_after"},
            timeout=self.timeout,
        )
        res.raise_for_status()
        logger.info("Customer with id <%s> deleted", customer_id)
        return res
