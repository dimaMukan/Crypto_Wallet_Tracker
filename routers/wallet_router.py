from fastapi import Depends
from models.wallet_mod import Wallet
from crud.wallet_curd import update_wallet, get_wallet
from fastapi import APIRouter, Depends
from schemas import schema_wallet
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from db.database import get_db

router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.patch("/{wallet_id}", response_model=schema_wallet.Wallet)
def patch_wallet(wallet_id: int, wallet_update: schema_wallet.WalletUpdate, db: Session = Depends(get_db)):
    wallet = get_wallet(wallet_id, db)
    updated_wallet = update_wallet(db, wallet, wallet_update)
    return updated_wallet
