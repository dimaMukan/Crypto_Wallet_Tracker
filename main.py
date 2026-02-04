from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import models,schemas
from db.database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_wallet(wallet_id: int, db: Session = Depends(get_db)):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
    return wallet

@app.post("/wallets", response_model=schemas.Wallet)
def add_wallet(
        wallet:schemas.WalletCreate,
        db: Session = Depends(get_db)):

    existing_wallet = db.query(models.Wallet).filter(
        models.Wallet.address == wallet.address
    ).first()

    if existing_wallet:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wallet with this address already exists"
        )

    db_wallet = models.Wallet(
        address=wallet.address,
        chain=wallet.chain,
        label=wallet.label
    )

    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

@app.get("/wallets", response_model=list[schemas.Wallet])
def get_wallets(db: Session = Depends(get_db)):
    wallets = db.query(models.Wallet).all()
    if not wallets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Wallet not found")
    return wallets

@app.get("/wallets/{wallet_id}", response_model=schemas.Wallet)
def get_wallets(wallet: models.Wallet = Depends(get_wallet())):
    return wallet

@app.delete("/wallets/delete/{wallet_id}", response_model=schemas.Wallet)
def delete_wallet(wallet: models.Wallet = Depends(get_wallet), db: Session = Depends(get_db)):
    db.delete(wallet)
    db.commit()
    return wallet


