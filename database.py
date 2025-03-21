from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
import os

db_dir = os.getenv("DATABASE_PATH", "/data")
db_path = os.path.join(db_dir, "coupons.db")

engine = create_engine(f"sqlite:///{db_path}")

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

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