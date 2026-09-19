from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class FoodModel(Base):
    __tablename__ = "foods"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column()
    category: Mapped[str] = mapped_column(String(100))
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id")
    )