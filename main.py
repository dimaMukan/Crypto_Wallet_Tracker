from fastapi import FastAPI
from routers.wallet_router import router
from db.database import engine
from db.base import Base
app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(router)

