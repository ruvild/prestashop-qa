from clients.binshops.base_client import BaseClient
from test_data.product_test_data import ProductToCart
from playwright.sync_api import APIRequestContext


class CartClient(BaseClient):
    def __init__(self, request_context: APIRequestContext) -> None:
        super().__init__()
        self.endpoint = "cart"
        self.request = request_context

    def get_cart_contents(self) -> dict:
        url = self.build_url(self.endpoint)
        response = self.request.get(url)
        assert response.ok, f"Couldn't fetch cart: {response.status} {response.text()}"

        return response.json()

    def add_product_to_cart(self, product_data: ProductToCart) -> dict:
        url = self.build_url(self.endpoint)
        params = product_data.model_dump(exclude_none=True)
        response = self.request.get(url, params=params)
        assert (
            response.ok
        ), f"Couldn't add product to cart: {response.status} {response.text()}"

        return response.json()
