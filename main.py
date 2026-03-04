from fastapi import FastAPI
from routers.wallet_router import router as wallet_router
from routers.transaction_router import router as transaction_router
from db.database import engine
from db.base import Base
from models import Wallet, Transaction

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(wallet_router)
app.include_router(transaction_router)
