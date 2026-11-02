from clients.binshops.base_client import BaseClient
from test_data.product_test_data import ProductToCart
from playwright.sync_api import APIRequestContext
from schemas.cart_schemas import CartResponse


class CartClient(BaseClient):
    def __init__(self, request_context: APIRequestContext) -> None:
        super().__init__()
        self.endpoint = "cart"
        self.request = request_context

    def get_cart_contents(self) -> CartResponse:
        url = self.build_url(self.endpoint)
        response = self.request.get(url)
        assert response.ok, f"Couldn't fetch cart: {response.status} {response.text()}"
        cart_response = CartResponse.model_validate(response.json())

        return cart_response

    def add_product_to_cart(self, product_data: ProductToCart) -> CartResponse:
        url = self.build_url(self.endpoint)
        params = product_data.model_dump(exclude_none=True)
        response = self.request.get(url, params=params)
        assert (
            response.ok
        ), f"Couldn't add product to cart: {response.status} {response.text()}"
        cart_response = CartResponse.model_validate(response.json())

        return cart_response
