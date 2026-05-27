from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.database import Base


class User(Base):
    username : Mapped[str] = mapped_column(String(50), nullable=False)
    email : Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    hash_password : Mapped[str] = mapped_column(String(250), nullable=False)
    is_active : Mapped[bool] = mapped_column(default=True, server_default="true")
    refresh_token : Mapped[str] = mapped_column(String, nullable=True)
    username_telegram : Mapped[str | None] = mapped_column(String(150), nullable=True)




