from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date

class GuestBase(BaseModel):
    name: str
    email: str
    phone: str

class GuestCreate(GuestBase):
    pass

class GuestResponse(GuestBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class UnitBase(BaseModel):
    name: str
    description: str
    capacity: int

class UnitCreate(UnitBase):
    pass

class UnitResponse(UnitBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class ReservationBase(BaseModel):
    guest_id: int
    unit_id: int
    check_in_date: date
    check_out_date: date

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    guest_id: Optional[int] = None
    unit_id: Optional[int] = None
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None

class ReservationResponse(ReservationBase):
    id: int
    status: str
    
    model_config = ConfigDict(from_attributes=True) 