from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
import os

engine = create_engine(f"sqlite:///coupons.db")

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, unique=True, index=True)
    amount = Column(Float)

class CouponCreate(BaseModel):
    barcode: str
    amount: float
    
class CouponOut(BaseModel):
    id: int
    barcode: str
    amount: float

    class Config:
        from_attributes = True