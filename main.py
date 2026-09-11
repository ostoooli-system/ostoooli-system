from database import engine, get_db
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="نظام إدارة الأسطول",
    description="جهة برمجة التطبيقات لإدارة السائقين والمحافظ المالية"
)

# --- دالة التقييم والفرز الآلي لمستندات المندوب ---
def evaluate_driver_compliance(driver: models.Driver):
    missing = []
    
    if not driver.has_valid_license:
        missing.append("رخصة القيادة")
    if not driver.has_medical_check:
        missing.append("الفحص الطبي")
    if not driver.national_id:
        missing.append("الهوية / الإقامة")

    if missing:
        driver.status = "غير مكتمل الأوراق"
        driver.missing_documents = "، ".join(missing)
    else:
        driver.status = "جاهز للعمل"
        driver.missing_documents = "لا يوجد (مكتمل)"


@app.get("/")
def read_root():
    return {"message": "Fleet Management API is Running!"}


@app.post("/drivers/", response_model=schemas.DriverResponse, summary="إضافة سائق جديد")
def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    db_driver = db.query(models.Driver).filter(models.Driver.driver_code == driver.driver_code).first()
    if db_driver:
        raise HTTPException(status_code=400, detail="السائق مسجل بالفعل")
    
    new_driver = models.Driver(**driver.model_dump())
    
    # فحص الأوراق وتحديد الحالة تلقائياً
    evaluate_driver_compliance(new_driver)
    
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver


@app.get("/drivers/", response_model=List[schemas.DriverResponse])
def get_drivers(db: Session = Depends(get_db)):
    return db.query(models.Driver).all()


@app.post("/app-stats/", response_model=schemas.DriverAppStatsResponse)
def create_app_stats(stats: schemas.DriverAppStatsCreate, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(models.Driver.driver_code == stats.driver_code).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    new_stats = models.DriverAppStats(
        driver_id=driver.id,
        app_name="General App",
        orders_completed=stats.total_trips,
        cash_collected=stats.cash_collected
    )
    
    driver.wallet_balance += stats.cash_collected
    
    db.add(new_stats)
    db.commit()
    db.refresh(new_stats)
    return new_stats


@app.post("/wallet/settle/")
def settle_wallet(settlement: schemas.CashSettlementRequest, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(models.Driver.driver_code == settlement.driver_code).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    driver.wallet_balance -= settlement.amount_paid
    db.commit()
    return {"message": "Settlement successful", "remaining_balance": driver.wallet_balance}