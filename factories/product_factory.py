from schemas.product_schemas import ProductCreateRequest
from faker import Faker

fake = Faker()


class ProductFactory:

    @staticmethod
    def create_product() -> ProductCreateRequest:
        return ProductCreateRequest(
            type="standard", names={"en-US": f"{fake.sentence(nb_words=10)}"}
        )
