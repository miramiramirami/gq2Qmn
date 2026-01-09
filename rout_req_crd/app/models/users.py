from db.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(50), nullable=False)
    email: Mapped[int] = mapped_column(String(150), index=True, unique=True)