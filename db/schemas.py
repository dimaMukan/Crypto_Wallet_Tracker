from pydantic import BaseModel
from typing import Optional

#post
class WalletCreate(BaseModel):
    address: str
    chain: str
    label: str | None = None

#get
class Wallet(BaseModel):
    id: int
    address: str
    chain: str
    label: str | None = None
    class Config:
        from_attributes = True

class WalletUpdate(BaseModel):
    name: Optional[str] = None
    balance: Optional[float] = None
    class Config:
        from_attributes = True