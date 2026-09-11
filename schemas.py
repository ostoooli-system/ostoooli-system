from pydantic import BaseModel, ConfigDict
from typing import Optional

# Base Driver Schema
class DriverBase(BaseModel):
    name: str
    driver_code: str
    phone: Optional[str] = None
    national_id: Optional[str] = None
    sponsorship_expiry_date: Optional[str] = None
    has_valid_license: bool = False
    has_medical_check: bool = False

# Schema for creating a new Driver
class DriverCreate(DriverBase):
    pass

status: str = "غير مكتمل الأوراق"
missing_documents: str = ""
# Schema for returning Driver details (Response)
class DriverResponse(DriverBase):
    id: int
    wallet_balance: float

    model_config = ConfigDict(from_attributes=True)


# Schema for App Stats Input
class DriverAppStatsCreate(BaseModel):
    driver_code: str
    total_trips: int
    cash_collected: float
    app_commission: float

# Schema for App Stats Response
class DriverAppStatsResponse(DriverAppStatsCreate):
    id: int
    driver_id: int

    model_config = ConfigDict(from_attributes=True)


# Schema for Cash Settlement Request
class CashSettlementRequest(BaseModel):
    driver_code: str
    amount_paid: float