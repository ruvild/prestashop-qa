import logging

from requests import Response

from clients.admin_api.base_client import BaseClient
from schemas.product_schemas import (
    ProductCombinationResponse,
    ProductCreateRequest,
    ProductListResponse,
    ProductPatchRequest,
    ProductResponse,
)
from test_data.product_test_data import TestCategory

logger = logging.getLogger(__name__)


class ProductsClient(BaseClient):
    def __init__(self, auth_token: str) -> None:
        super().__init__(auth_token)
        self.endpoint = "products"

    def get_product(self, product_id: int) -> ProductResponse:
        url = self.build_url(f"{self.endpoint}/{product_id}")
        res = self.session.get(url, headers=self.auth_header, timeout=self.timeout)
        res.raise_for_status()
        return ProductResponse.model_validate(res.json())

    def create_product(self, product: ProductCreateRequest) -> ProductResponse:
        url = self.build_url(self.endpoint)
        payload = product.model_dump(exclude_none=True)
        res = self.session.post(
            url, headers=self.auth_header, json=payload, timeout=self.timeout
        )
        res.raise_for_status()

        product_data: dict = res.json()
        logger.info(
            "Product %s created with id: %s",
            product_data["names"]["en-US"],
            product_data.get("productId"),
        )
        return ProductResponse.model_validate(product_data)

    def delete_product(self, product_id: int) -> Response:
        url = self.build_url(f"{self.endpoint}/{product_id}")
        res = self.session.delete(url, headers=self.auth_header, timeout=self.timeout)
        res.raise_for_status()

        logger.info("Product with id <%s> deleted", product_id)
        return res

    def update_product(self, product_id: int, patch_data: dict) -> ProductResponse:
        url = self.build_url(f"{self.endpoint}/{product_id}")
        validated_patch_data = ProductPatchRequest.model_validate(patch_data)
        payload: dict = validated_patch_data.model_dump(exclude_none=True)
        res = self.session.patch(
            url, headers=self.auth_header, json=payload, timeout=self.timeout
        )
        res.raise_for_status()

        product_data: dict = res.json()
        logger.info(
            "Product with id <%s> updated with new data: %s", product_id, payload
        )
        return ProductResponse.model_validate(product_data)

    def filter_products_by_category(self, category: TestCategory) -> set[int]:
        url = self.build_url(self.endpoint)
        res = self.session.get(url, headers=self.auth_header, timeout=self.timeout)
        res.raise_for_status()

        data = ProductListResponse.model_validate(res.json())
        return {
            product.productId
            for product in data.items
            if product.category == category.name
        }

    def search_product_combination(
        self, combination_id: int
    ) -> ProductCombinationResponse:
        url = self.build_url(f"{self.endpoint}/combinations/{combination_id}")
        res = self.session.get(url, headers=self.auth_header, timeout=self.timeout)
        res.raise_for_status()

        return ProductCombinationResponse.model_validate(res.json())
