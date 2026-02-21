from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.wallet_mod import Wallet
from schemas.schema_wallet import WalletUpdate, WalletCreate


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

def delete_wallet(db: Session, wallet_id: int):
    wallet = get_wallet(wallet_id, db)
    db.delete(wallet)
    db.commit()
    return wallet

def add_wallet(db: Session, wallet_create: WalletCreate):
    existing_wallet = db.query(Wallet).filter(
        Wallet.address == wallet_create.address
    ).first()

    if existing_wallet:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Wallet with this address already exists")
    db_wallet = Wallet(**wallet_create.model_dump(exclude_unset=True))
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet


