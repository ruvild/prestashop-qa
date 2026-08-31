from dataclasses import dataclass


@dataclass(frozen=True)
class TestCategory:
    name: str
    id: int


ACCESSORIES = TestCategory("Accessories", 6)
STATIONERY = TestCategory("Stationery", 7)
HOME_ACCESSORIES = TestCategory("Home Accessories", 8)
