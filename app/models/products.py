from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric
from decimal import Decimal
from app.database import Base 

class Product(Base):
    name : Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description : Mapped[str] = mapped_column(String, nullable=False)
    price : Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=2), nullable=False)
    img_url : Mapped[str]

