from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, func
from db.base import Base

class HolderTransactionEvent(Base):
    __tablename__ = "HolderTransactionEvent"
    id = Column(Integer, primary_key=True, index=True)
    holder_id = Column(Integer, ForeignKey("TrackedHolder.id"), nullable=False, index=True)
    transaction_hash = Column(String, nullable=False, index=True)
    direction = Column(String, nullable=False)  # IN / OUT / SELF
    from_address = Column(String, nullable=False, index=True)
    to_address = Column(String, nullable=True, index=True)
    block_number = Column(Integer, nullable=False, index=True)
    block_timestamp = Column(DateTime, nullable=False)
    value_raw = Column(String, nullable=False)
    token_symbol = Column(String, nullable=False, default="USDC")
    token_decimals = Column(Integer, nullable=False, default=6)
    contract_address = Column(String, nullable=False)
    source = Column(String, nullable=False, default="etherscan")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "holder_id",
            "transaction_hash",
            "from_address",
            "to_address",
            "value_raw",
            name="uq_holder_transfer_event",
        ),
    )