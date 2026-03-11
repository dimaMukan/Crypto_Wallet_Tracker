from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from routers.wallet_router import router as wallet_router
from routers.transaction_router import router as transaction_router
from db.database import engine
from db.base import Base
from models import Wallet, Transaction
from routers.TrackedHolder_router import router as tracked_holder_router


app = FastAPI()
# Base.metadata.create_all(bind=engine)


@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(Path(__file__).parent / "frontend" / "index.html")


app.include_router(wallet_router)
app.include_router(transaction_router)
app.include_router(tracked_holder_router)

