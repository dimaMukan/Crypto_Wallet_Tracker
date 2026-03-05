from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, func
from db.base import Base

class HolderTransactionEvent(Base):
    __tablename__ = "HolderTransactionEvent"
    id = Column(Integer, primary_key=True, index=True)
    holder_id = Column(Integer, ForeignKey("TrackedHolder.id"), nullable=False, index=True)
    transaction_hash = Column(String, nullable=False, index=True)
    direction = Column(String, nullable=False)  # IN / OUT
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=True)
    value_wei = Column(String, nullable=False)
    block_number = Column(Integer, nullable=False, index=True)
    block_timestamp = Column(DateTime, nullable=False)
    notified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    __table_args__ = (
        UniqueConstraint("holder_id", "transaction_hash", name="uq_holder_transaction_hash"),

    )