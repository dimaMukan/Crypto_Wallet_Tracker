from datetime import datetime
from pydantic import BaseModel

class TrackedHolderOut(BaseModel):
    id: int
    address: str
    rank: int
    balance_wei: str
    source: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True