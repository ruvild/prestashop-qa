from uuid import uuid4

from schemas.product_schemas import ProductCreateRequest


class ProductFactory:

    @staticmethod
    def create_base_product() -> ProductCreateRequest:
        return ProductCreateRequest(
            type="standard",
            names={"en-US": f"Test Mug {uuid4().hex[:8]}"},
        )
