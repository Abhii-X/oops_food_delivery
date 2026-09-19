from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )
    food_id: Mapped[int] = mapped_column(
        ForeignKey("foods.id")
    )
    quantity: Mapped[int] = mapped_column()