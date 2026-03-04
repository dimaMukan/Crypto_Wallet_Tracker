from pydantic import BaseModel
from datetime import datetime


class TransactionBase(BaseModel):
    hash: str
    from_address: str
    to_address: str
    value: float
    gas: float
    gas_price: float
    block_number: int


class TransactionCreate(TransactionBase):
    wallet_id: int
    timestamp: datetime | None = None


class Transaction(TransactionBase):
    id: int
    wallet_id: int
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionUpdate(BaseModel):
    hash: str | None = None
    from_address: str | None = None
    to_address: str | None = None
    value: float | None = None
    gas: float | None = None
    gas_price: float | None = None
    block_number: int | None = None
    timestamp: datetime | None = None
    wallet_id: int | None = None

    class Config:
        from_attributes = True
