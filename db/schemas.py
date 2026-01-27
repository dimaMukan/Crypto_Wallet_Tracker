from pydantic import BaseModel

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