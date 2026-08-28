from clients.admin_api.base_client import BaseClient
from schemas.product_schemas import (
    ProductCreateRequest,
    ProductResponse,
    ProductPatchRequest,
)
from requests import Response


class ProductsClient(BaseClient):
    def __init__(self, auth_token: str) -> None:
        super().__init__(auth_token)
        self.endpoint = "products"

    def create_product(self, product: ProductCreateRequest):
        url = self.build_url(self.endpoint)
        payload = product.model_dump(exclude_none=True)
        res = self.session.post(url, headers=self.auth_header, json=payload)
        res.raise_for_status()

        product_data: dict = res.json()
        print(
            f"Product {product_data['names']['en-US']} created with id: {product_data.get('productId')}"
        )
        return ProductResponse.model_validate(product_data)

    def delete_product(self, product_id: int) -> Response:
        url = self.build_url(f"{self.endpoint}/{product_id}")
        res = self.session.delete(url, headers=self.auth_header)
        res.raise_for_status()

        print(f"Product with id <{product_id}> deleted")
        return res

    def update_product(self, product_id: int, patch_data: dict):
        url = self.build_url(f"{self.endpoint}/{product_id}")
        validated_patch_data = ProductPatchRequest.model_validate(patch_data)
        payload: dict = validated_patch_data.model_dump(exclude_none=True)
        res = self.session.patch(url, headers=self.auth_header, json=payload)
        res.raise_for_status()

        product_data: dict = res.json()
        print(f"Product with id <{product_id}> updated with new data: {payload}")
        return ProductResponse.model_validate(product_data)
