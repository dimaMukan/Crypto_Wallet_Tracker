from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import schema_wallet
from models.wallet_mod import Wallet
from schemas.schema_wallet import WalletUpdate
from db.database import get_db


def get_wallets(db: Session):
    wallets = db.query(Wallet).all()
    if not wallets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
    return wallets

def get_wallet(wallet_id: int, db: Session):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
    return wallet


def update_wallet(db: Session, wallet: Wallet, wallet_update: WalletUpdate):
    updated_wallet = wallet_update.model_dump(exclude_unset=True)
    for key, value in updated_wallet.items():
        setattr(wallet, key, value)
    db.commit()
    db.refresh(wallet)
    return wallet



