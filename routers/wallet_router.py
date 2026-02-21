from models.wallet_mod import Wallet
from schemas import schema_wallet
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from db.database import get_db
from crud.wallet_crud import update_wallet, get_wallet,add_wallet

router = APIRouter(prefix="/wallets", tags=["wallets"])

@router.patch("/{wallet_id}", response_model=schema_wallet.Wallet)
def patch_wallet_router(wallet_id: int, wallet_update: schema_wallet.WalletUpdate, db: Session = Depends(get_db)):
    wallet = get_wallet(wallet_id, db)
    updated_wallet = update_wallet(db, wallet, wallet_update)
    return updated_wallet

@router.get("/", response_model=list[schema_wallet.Wallet])
def get_wallets_router(db: Session = Depends(get_db)):
    wallets = db.query(Wallet).all()
    return wallets

@router.get("/{wallet_id}", response_model=schema_wallet.Wallet)
def get_wallet_router(wallet_id: int,db: Session = Depends(get_db)):
    wallet = get_wallet(wallet_id, db)
    return wallet

@router.delete("/{wallet_id}", response_model=schema_wallet.Wallet)
def delete_wallet_router(wallet_id: int,db: Session = Depends(get_db)):
    wallet = get_wallet(wallet_id, db)
    db.delete(wallet)
    db.commit()
    return wallet

@router.post("/", response_model=schema_wallet.Wallet)
def add_wallet_router(wallet: schema_wallet.WalletCreate, db: Session = Depends(get_db)):
    return add_wallet(db, wallet)

