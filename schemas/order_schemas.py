from pydantic import BaseModel


class OrderProduct(BaseModel):
    id_product: int
    product_attribute_id: int | None = None
    quantity: int
    product_name: str


class DeliveryAddress(BaseModel):
    id_customer: int


class OrderAddresses(BaseModel):
    delivery: DeliveryAddress


class OrderShippingItem(BaseModel):
    carrier_name: str


class OrderDetails(BaseModel):
    id: int
    reference: str
    payment: str
    shipping: list[OrderShippingItem]


class TotalIncludingTax(BaseModel):
    value: str


class OrderTotals(BaseModel):
    total_including_tax: TotalIncludingTax


class OrderData(BaseModel):
    products: dict[str, OrderProduct]
    addresses: OrderAddresses
    details: OrderDetails
    totals: OrderTotals


class OrderResponse(BaseModel):
    success: bool
    code: int
    psdata: OrderData
