from clients.binshops.base_client import BaseClient
from typing import Any


class ProductSearchClient(BaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.endpoint = "productSearch"

    def search_products(
        self,
        sort_order: str | None = None,
        results_per_page: int | None = None,
        page: int | None = None,
        query: str = "hummingbird",
    ) -> dict[str, Any]:

        params = {
            "s": query,
            "resultsPerPage": results_per_page,
            "page": page,
            "order": sort_order,
        }

        params = {key: value for key, value in params.items() if value is not None}

        url = self.build_url(self.endpoint)
        res = self.session.get(url, params=params)
        res.raise_for_status()
        return res.json()
