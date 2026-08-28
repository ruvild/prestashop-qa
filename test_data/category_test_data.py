from dataclasses import dataclass


@dataclass(frozen=True)
class TestCategory:
    name: str
    id: int


@dataclass(frozen=True)
class TestSubcategory:
    name: str
    id: int


ACCESSORIES = TestCategory("Accessories", 6)
STATIONERY = TestSubcategory("Stationery", 7)
HOME_ACCESSORIES = TestSubcategory("Home Accessories", 8)
