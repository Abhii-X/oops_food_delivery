from pydantic import BaseModel


class DeliveryRequest(BaseModel):
    order_id: int