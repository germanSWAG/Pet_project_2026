from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, CheckConstraint, Integer
from app.database import Base


class SearchFilter(Base):
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    brand : Mapped[str] = mapped_column(String(60), nullable=False)
    model : Mapped[str] = mapped_column(String(60), nullable=False)
    equipment : Mapped[str | None] = mapped_column(String(260), default=None)
    max_price : Mapped[int] = mapped_column(Integer, CheckConstraint("max_price>=10000"), nullable=False)
    min_year : Mapped[int | None] = mapped_column(CheckConstraint("min_year>=1899"), default=None)

    is_active : Mapped[bool] = mapped_column(default=True)


