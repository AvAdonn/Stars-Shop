from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    spent_money: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))
    referral_id: Mapped[BigInteger | None] = mapped_column(BigInteger, ForeignKey('users.tg_id', ondelete='SET NULL'), nullable=True, index=True) 
    language: Mapped[str] = mapped_column(String)
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    
    def __repr__(self) -> str:
        return f'<User(tg_id={self.tg_id}, spent_money={self.spent_money}>'