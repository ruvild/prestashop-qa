from clients.binshops.base_client import BaseClient
from typing import Any


class ProductSearchClient(BaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.endpoint = "productSearch"

    def search_products(
        self, sort_order: dict | None = None, query: str = "hummingbird"
    ) -> dict[str, Any]:
        url = self.build_url(self.endpoint)
        params = {"s": query}
        if sort_order:
            params |= sort_order
        res = self.session.get(url, params=params)
        res.raise_for_status()
        return res.json()
