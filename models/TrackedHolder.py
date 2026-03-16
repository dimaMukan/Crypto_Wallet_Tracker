from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from db.base import Base

class TrackedHolder(Base):
    __tablename__ = "TrackedHolder"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False, unique=True, index=True)
    rank = Column(Integer, nullable=False, index=True)
    # Keep the existing DB column name for compatibility, but expose USDC semantics in code.
    balance_raw = Column("balance_wei", String, nullable=False)
    source = Column(String, nullable=False, default="dune")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
