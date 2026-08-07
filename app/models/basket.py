from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from app.database import Base

if TYPE_CHECKING:
    from .products import Product
    
class Basket(Base):
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    product_id : Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    quantity : Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    product : Mapped['Product'] = relationship()

    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='idx_user_id_product_id')
    )