from schemas.product_schemas import ProductCreateRequest


class ProductFactory:

    @staticmethod
    def create_base_product() -> ProductCreateRequest:
        return ProductCreateRequest(type="standard", names={"en-US": "Test Mug"})
