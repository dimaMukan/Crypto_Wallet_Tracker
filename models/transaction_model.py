from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from datetime import datetime
from db.base import Base

class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, unique=True, nullable=False, index=True)
    wallet_id = Column(Integer, ForeignKey('wallet.id'), nullable=False)
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    gas = Column(Float, nullable=False)
    gas_price = Column(Float, nullable=False)
    block_number = Column(Integer, nullable=False)
    timestamp = Column(DateTime,default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow, nullable=False)

    wallet = relationship("Wallet",
                          back_populates="transactions")