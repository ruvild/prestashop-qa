from dataclasses import dataclass
from pydantic import BaseModel
from typing import Literal
import pytest


@dataclass(frozen=True)
class TestCategory:
    name: str
    id: int


ACCESSORIES = TestCategory("Accessories", 6)
STATIONERY = TestCategory("Stationery", 7)
HOME_ACCESSORIES = TestCategory("Home Accessories", 8)


class ProductToCart(BaseModel):
    update: Literal[1] = 1
    id_product: int
    id_product_attribute: int | None = None
    op: Literal["up", "down"]
    action: Literal["update"] = "update"
    qty: int


ADD_PRODUCT_TO_CART = ProductToCart(
    id_product=2, id_product_attribute=11, op="up", qty=2
)


class ProductTestData:

    SEARCH_QUERIES_ERROR = [
        pytest.param("", id="empty"),
        pytest.param("0", id="zero"),
    ]

    SEARCH_QUERIES_NO_MATCHES = [
        pytest.param("m", id="single_character"),
        pytest.param("mu", id="two_characters"),
        pytest.param("zzznomatch", id="no_matches"),
    ]

    SEARCH_QUERIES_MATCH_FOUND = [
        pytest.param("mug", id="normal"),
        pytest.param("MUG", id="uppercase"),
    ]

    PRODUCT_SORTING_METHODS = [
        pytest.param("position", "product.position.desc", id="relevance"),
        pytest.param("name", "product.name.asc", id="name_asc"),
        pytest.param("name", "product.name.desc", id="name_desc"),
        pytest.param("price", "product.price.asc", id="price_asc"),
        pytest.param("price", "product.price.desc", id="price_desc"),
    ]

    PRODUCT_PRICE_RANGES_EXIST = [
        pytest.param(10, 40, id="all_products"),
        pytest.param(11.9, 18.9, id="some_products"),
        pytest.param(30, 35.5, id="most_expensive_product"),
        pytest.param(18.9, 18.9, id="single_price"),
    ]

    PRODUCT_PRICE_RANGES_NOT_EXIST = [
        pytest.param(12, 13, id="no_products_in_between"),
        pytest.param(36, 40, id="no_products_above"),
        pytest.param(10, 11.89, id="no_products_below"),
    ]
