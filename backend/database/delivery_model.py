from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class DeliveryModel(Base):
    __tablename__ = "deliveries"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )
    address: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(50))