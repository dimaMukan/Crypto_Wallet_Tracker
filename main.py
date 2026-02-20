from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
# main.py
from routers.wallet_router import router
from models.wallet_mod import Wallet
from db.database import engine, SessionLocal
from db.base import Base
from db.database import get_db
from crud.wallet_curd import update_wallet, get_wallet

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(router)








# def get_wallet(wallet_id: int, db: Session = Depends(get_db)):
#     wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
#     if not wallet:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
#     return wallet
#
# @app.post("/wallets", response_model=schema_wallet.Wallet)
# def add_wallet(
#         wallet: schema_wallet.WalletCreate,
#         db: Session = Depends(get_db)):
#
#     existing_wallet = db.query(Wallet).filter(
#         Wallet.address == wallet.address
#     ).first()
#
#     if existing_wallet:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="Wallet with this address already exists"
#         )
#
#     db_wallet = Wallet(
#         address=wallet.address,
#         chain=wallet.chain,
#         label=wallet.label
#     )
#
#     db.add(db_wallet)
#     db.commit()
#     db.refresh(db_wallet)
#     return db_wallet
#
# @app.get("/wallets", response_model=list[schema_wallet.Wallet])
# def get_wallets(db: Session = Depends(get_db)):
#     wallets = db.query(Wallet).all()
#     if not wallets:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Wallet not found")
#     return wallets
#
# @app.get("/wallets/{wallet_id}", response_model=schema_wallet.Wallet)
# def get_wallet(wallet: Wallet = Depends(get_wallet)):
#     return wallet
#
# @app.delete("/wallets/delete/{wallet_id}", response_model=schema_wallet.Wallet)
# def delete_wallet(wallet: Wallet = Depends(get_wallet), db: Session = Depends(get_db)):
#     db.delete(wallet)
#     db.commit()
#     return wallet
# #
# @app.patch("/wallets/{wallet_id}", response_model=schema_wallet.Wallet)
# def update_wallet(wallet_update: schema_wallet.WalletUpdate,
#                   wallet: Wallet = Depends(get_wallet),
#                   db: Session = Depends(get_db)
#                   ):
#     update_data = wallet_update.model_dump(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(wallet, key, value)
#     db.commit()
#     db.refresh(wallet)
#     return wallet
#

