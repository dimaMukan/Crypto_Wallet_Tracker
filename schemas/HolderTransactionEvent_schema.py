from datetime import datetime
from pydantic import BaseModel


class HolderTransactionEventOut(BaseModel):
    id: int
    holder_id: int
    transaction_hash: str
    direction: str
    from_address: str
    to_address: str | None
    block_number: int
    block_timestamp: datetime
    value_raw: str
    token_symbol: str
    token_decimals: int
    contract_address: str
    source: str
    created_at: datetime

    class Config:
        from_attributes = True
