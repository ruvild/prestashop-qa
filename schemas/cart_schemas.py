from typing import Literal

from pydantic import BaseModel


class ProductToCart(BaseModel):
    update: Literal[1] = 1
    id_product: int
    id_product_attribute: int | None = None
    op: Literal["up", "down"]
    action: Literal["update"] = "update"
    qty: int


class CartProduct(BaseModel):
    id_product: int
    id_product_attribute: int | None = None
    cart_quantity: int


class CartData(BaseModel):
    products: list[CartProduct]
    errors: list[str]


class CartResponse(BaseModel):
    success: bool
    psdata: CartData
