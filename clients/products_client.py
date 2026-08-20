from clients.base_client import BaseClient
from schemas.product_schemas import ProductCreateRequest, ProductResponse


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
