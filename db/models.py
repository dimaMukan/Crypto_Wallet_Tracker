from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class Wallet(Base):
    __tablename__ = "wallet"
    id = Column(Integer, primary_key=True,index=True)
    address = Column(String,unique=True,index=True)
    chain = Column(String,index=True)
    label = Column(String,nullable=False)