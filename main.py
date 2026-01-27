from fastapi import FastAPI, Depends
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

@app.post("/wallets", response_model=schemas.Wallet)
def add_wallet(
        wallet:schemas.WalletCreate,
        db: Session = Depends(get_db)):
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
    return db.query(models.Wallet).all()