from sqlalchemy import Column, Integer, String, DateTime
from db.base import Base
from .mixins import TimestampMixin

class Wallet(Base, TimestampMixin):
    __tablename__ = "wallet"
    id = Column(Integer, primary_key=True,index=True)
    address = Column(String,unique=True,index=True)
    chain = Column(String,index=True,nullable=False)
    label = Column(String,nullable=False)
