from pydantic import BaseModel
from typing import Literal


class ProductCreateRequest(BaseModel):
    type: Literal["standard", "pack", "virtual", "combinations"]
    names: dict[str, str]


class ProductCategory(BaseModel):
    categoryId: int
    name: str
    displayName: str


class ProductPatchRequest(BaseModel):
    enabled: bool | None = None
    descriptions: dict[str, str] | None = None
    priceTaxExcluded: float | None = None
    onSale: bool | None = None
    visibility: Literal["both", "catalog", "search", "none"] | None = None
    availableForOrder: bool | None = None
    reference: str | None = None


class ProductResponse(ProductCreateRequest):
    productId: int
    enabled: bool
    descriptions: dict[str, str]
    priceTaxExcluded: float
    quantity: int
    onSale: bool
    visibility: Literal["both", "catalog", "search", "none"]
    availableForOrder: bool
    reference: str
    categories: list[ProductCategory]
