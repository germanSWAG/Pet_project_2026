from sqlalchemy.orm import Mapped
from app.database import Base 

class Product(Base):
    name : Mapped[str] 
    description : Mapped[str]
    price : Mapped[float]
    img_url : Mapped[str]

