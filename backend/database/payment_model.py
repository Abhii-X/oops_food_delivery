from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class PaymentModel(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )
    amount: Mapped[float] = mapped_column()
    method: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50))