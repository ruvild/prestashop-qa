from factories.product_factory import ProductFactory


def test_product(products_client):
    product = ProductFactory.create_base_product()
    product_response = products_client.create_product(product)
    assert "productId" in product_response.model_dump()
