from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base 

class Product(Base):
    name : Mapped[str] 
    description : Mapped[str]
    price : Mapped[float]
    img_url : Mapped[str]

