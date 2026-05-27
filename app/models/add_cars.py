from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class AdsCar(Base):
    platform : Mapped[str] = mapped_column(String(60), nullable=False)
    brand : Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    model : Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    equipment : Mapped[str | None] = mapped_column(String(260), nullable=True)
    price : Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    url : Mapped[str] = mapped_column(Text, nullable=False, unique=True)
