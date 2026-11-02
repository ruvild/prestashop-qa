from clients.binshops.base_client import BaseClient
from test_data.product_test_data import TestCategory
from typing import Any


class CategoryProductsClient(BaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.endpoint = "categoryProducts"

    def search_category_products(
        self,
        category: TestCategory,
        additional_filters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = self.build_url(self.endpoint)
        params = {"id_category": category.id}
        if additional_filters:
            params |= additional_filters
        res = self.session.get(url, params=params)
        res.raise_for_status()

        return res.json()
