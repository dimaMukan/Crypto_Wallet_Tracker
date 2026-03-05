from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

UNIQUE_ERROR_MAP = {
    "wallet.address": "Wallet address already exists",
    "transaction.hash": "Transaction hash already exists",
    "TrackedHolder.address": "Tracked holder address already exists",
    "uq_holder_transaction_hash": "This holder transaction is already saved",
}

def raise_integrity_error(error: IntegrityError) -> None:
    msg = str(error.orig)
    for key, value in UNIQUE_ERROR_MAP.items():
        if key in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=value)
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Database integrity error")


