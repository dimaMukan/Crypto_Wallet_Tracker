from pydantic import BaseModel
from typing import Optional
from enum import Enum

class ChainEnum(str,Enum):
    ethereum = "ethereum"
    solana = "solana"
    btc = "btc"
#post
class WalletCreate(BaseModel):
    address: str
    chain: ChainEnum
    label: str | None = None

#get
class Wallet(BaseModel):
    id: int
    address: str
    chain: ChainEnum
    label: str | None = None
    class Config:
        from_attributes = True

#update
class WalletUpdate(BaseModel):
    address: Optional[str] = None
    chain: ChainEnum | None = None
    label: Optional[str] = None
    class Config:
        from_attributes = True