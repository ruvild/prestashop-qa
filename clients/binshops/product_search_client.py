from clients.binshops.base_client import BaseClient


class ProductSearchClient(BaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.endpoint = "productSearch"

    def search_products(self, query: str):
        url = self.build_url(self.endpoint)
        params = {"s": query}
        res = self.session.get(url, params=params)
        res.raise_for_status()
        return res.json()
