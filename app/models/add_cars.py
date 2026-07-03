from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class AdsCar(Base):
    brand : Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    model : Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    price : Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    city : Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    year : Mapped[int] = mapped_column(Integer, nullable=False)
    url : Mapped[str] = mapped_column(Text, nullable=False, unique=True)
