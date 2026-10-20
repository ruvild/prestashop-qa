from dataclasses import dataclass
import pytest


@dataclass(frozen=True)
class TestCategory:
    name: str
    id: int


ACCESSORIES = TestCategory("Accessories", 6)
STATIONERY = TestCategory("Stationery", 7)
HOME_ACCESSORIES = TestCategory("Home Accessories", 8)


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
