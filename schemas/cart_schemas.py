from pydantic import BaseModel


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
