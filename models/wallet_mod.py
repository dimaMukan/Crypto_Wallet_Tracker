from sqlalchemy import Column, Integer, String
from db.base import Base
from .mixins import TimestampMixin
from sqlalchemy.orm import relationship


class Wallet(Base, TimestampMixin):
    __tablename__ = "wallet"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    chain = Column(String, index=True, nullable=False)
    label = Column(String, nullable=False)

    transactions = relationship(
        "Transaction",
        back_populates="wallet",
        cascade="all, delete-orphan",
    )
