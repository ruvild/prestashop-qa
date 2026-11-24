from typing import Any

from clients.binshops.base_client import BaseClient
from schemas.product_schemas import BinshopsProductListResponse
from test_data.product_test_data import TestCategory


class CategoryProductsClient(BaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.endpoint = "categoryProducts"

    def search_category_products(
        self,
        category: TestCategory,
        additional_filters: dict[str, Any] | None = None,
    ) -> BinshopsProductListResponse:
        url = self.build_url(self.endpoint)
        params = {"id_category": category.id}
        if additional_filters:
            params |= additional_filters
        res = self.session.get(url, params=params, timeout=self.timeout)
        res.raise_for_status()

        return BinshopsProductListResponse.model_validate(res.json())
