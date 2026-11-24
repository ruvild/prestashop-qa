from typing import Literal

from pydantic import BaseModel, ConfigDict


class ProductCreateRequest(BaseModel):
    type: Literal["standard", "pack", "virtual", "combinations"]
    names: dict[str, str]


class ProductCategory(BaseModel):
    categoryId: int
    name: str
    displayName: str


class ProductPatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enabled: bool | None = None
    descriptions: dict[str, str] | None = None
    shortDescriptions: dict[str, str] | None = None
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


class ProductListItem(BaseModel):
    productId: int
    category: str


class ProductListResponse(BaseModel):
    items: list[ProductListItem]


class ProductCombinationResponse(BaseModel):
    combinationId: int
    productId: int
    name: str
    default: bool
    quantity: int
    reference: str


class BinshopsProduct(BaseModel):
    id_product: int
    name: str
    price: str
    position: str | None = None


class BinshopsProductData(BaseModel):
    products: list[BinshopsProduct]


class BinshopsProductListResponse(BaseModel):
    code: int
    success: bool
    psdata: BinshopsProductData | None = None
    message: str | None = None
