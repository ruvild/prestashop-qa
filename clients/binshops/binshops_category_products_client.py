from clients.binshops.binshops_base_client import BinshopsBaseClient
from test_data.category_test_data import HOME_ACCESSORIES


class CategoryProductsClient(BinshopsBaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.endpoint = "categoryProducts"

    def search_category_products(
        self,
        category_id: int = HOME_ACCESSORIES.id,
        additional_params: dict = {},
    ):
        url = self.build_url(f"self.endpoint")
        params = {"id_category": category_id}
        res = self.session.get(url, params=params | additional_params)
