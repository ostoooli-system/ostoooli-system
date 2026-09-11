from sqlalchemy import Column,Integer,String,Float,Date,ForeignKey,DateTime,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, date
from database import Base 
class Driver(Base): 
    __tablename__ =  "drivers"
    id=Column(Integer,primary_key=True, index=True)
    driver_code=Column(String, unique=True, index=True)
    name=Column(String, index=True)
    phone=Column(String, nullable=True)
    national_id=Column(String, nullable=True)
    sponsorship_expiry_date=Column(Date, nullable=False)
    sponsorship_expiry_date = Column(Date, nullable=True)
    has_valid_license = Column(Boolean, default=False)
    has_medical_check = Column(Boolean, default=False)
    status = Column(String, default="غير مكتمل الأوراق")
    missing_documents = Column(String, default="")
    transfer_requests_count = Column(Integer, default=0)
transfer_requests_count=Column(Integer, default=0)
last_transfer_date=Column(Date, nullable=True)
wallet_balance=Column(Float, default=0.0)
app_stats=relationship("DriverAppStats", back_populates="driver")
class DriverAppStats(Base):
        __tablename__="driver_platform_stats"
        id=Column(Integer, primary_key=True, index=True)
        driver_id=Column(Integer,ForeignKey("drivers.id"))
        app_name= Column(String, nullable=False)
        working_hours=Column(Float, default=0.0)
        orders_completed=Column(Integer,default=0)
        cash_collected=Column(Float,default=0.0)
        submission_date=Column(Date,nullable=True)
        updated_at=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        driver= relationship("Driver", back_populates="app_stats")