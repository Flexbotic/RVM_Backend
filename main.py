from fastapi import FastAPI, HTTPException, Header
from typing import List
import re
from database import Coupon, CouponCreate, CouponOut, SessionLocal

API_KEY = "FXXBBAPIK2213"

app = FastAPI()

@app.post("/add_coupon")
def add_coupon(coupon: CouponCreate, x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not re.match(r"^BUT[a-zA-Z0-9]{1,10}$", coupon.barcode):
        raise HTTPException(status_code=400, detail="Invalid barcode format")

    db = SessionLocal()
    if db.query(Coupon).filter_by(barcode=coupon.barcode).first():
        raise HTTPException(status_code=400, detail="Barcode already exists")

    db_coupon = Coupon(barcode=coupon.barcode, amount=coupon.amount)
    db.add(db_coupon)
    db.commit()
    db.close()
    return {"status": "success", "barcode": coupon.barcode}

@app.get("/coupons", response_model=List[CouponOut])
def get_coupons(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    db = SessionLocal()
    coupons = db.query(Coupon).all()
    db.close()
    return coupons