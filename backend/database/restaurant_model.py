from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class RestaurantModel(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(200))