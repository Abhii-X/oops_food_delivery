from pydantic import BaseModel


class OrderItemRequest(BaseModel):
    food_id: int
    quantity: int


class OrderCreateRequest(BaseModel):
    customer_id: int
    items: list[OrderItemRequest]