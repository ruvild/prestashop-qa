from clients.binshops.base_client import BaseClient
from test_data.product_test_data import TestCategory
from typing import Any
from config.utils import binshops_extractor


class CategoryProductsClient(BaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.endpoint = "categoryProducts"

    def search_category_products(
        self,
        category: TestCategory,
        additional_params: dict[str, Any] | None = None,
    ) -> set:
        url = self.build_url(self.endpoint)
        params = {"id_category": category.id}
        if additional_params:
            params |= additional_params
        res = self.session.get(url, params=params)
        res.raise_for_status()

        data: dict[str, Any] = res.json()
        return set(binshops_extractor("id_product", data))
