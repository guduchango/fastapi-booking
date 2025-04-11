from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import os

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./reservations.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
class Guest(Base):
    __tablename__ = "guests"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    reservations = relationship("Reservation", back_populates="guest")

class Unit(Base):
    __tablename__ = "units"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    capacity = Column(Integer)
    reservations = relationship("Reservation", back_populates="unit")

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, ForeignKey("guests.id"))
    unit_id = Column(Integer, ForeignKey("units.id"))
    check_in_date = Column(Date)
    check_out_date = Column(Date)
    status = Column(String, default="active")
    
    guest = relationship("Guest", back_populates="reservations")
    unit = relationship("Unit", back_populates="reservations")

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class GuestBase(BaseModel):
    name: str
    email: str
    phone: str

class GuestCreate(GuestBase):
    pass

class GuestResponse(GuestBase):
    id: int
    
    class Config:
        from_attributes = True

class UnitBase(BaseModel):
    name: str
    description: str
    capacity: int

class UnitCreate(UnitBase):
    pass

class UnitResponse(UnitBase):
    id: int
    
    class Config:
        from_attributes = True

class ReservationBase(BaseModel):
    guest_id: int
    unit_id: int
    check_in_date: date
    check_out_date: date

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    id: int
    status: str
    
    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to check for overlapping reservations
def has_overlapping_reservation(db: Session, unit_id: int, check_in: date, check_out: date, exclude_reservation_id: Optional[int] = None):
    query = db.query(Reservation).filter(
        Reservation.unit_id == unit_id,
        Reservation.status == "active",
        Reservation.check_in_date < check_out,
        Reservation.check_out_date > check_in
    )
    
    if exclude_reservation_id:
        query = query.filter(Reservation.id != exclude_reservation_id)
    
    return query.first() is not None

# API endpoints
@app.post("/guests/", response_model=GuestResponse)
def create_guest(guest: GuestCreate, db: Session = Depends(get_db)):
    db_guest = Guest(**guest.model_dump())
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest

@app.get("/guests/", response_model=List[GuestResponse])
def read_guests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    guests = db.query(Guest).offset(skip).limit(limit).all()
    return guests

@app.post("/units/", response_model=UnitResponse)
def create_unit(unit: UnitCreate, db: Session = Depends(get_db)):
    db_unit = Unit(**unit.model_dump())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

@app.get("/units/", response_model=List[UnitResponse])
def read_units(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    units = db.query(Unit).offset(skip).limit(limit).all()
    return units

@app.post("/reservations/", response_model=ReservationResponse)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    # Check if the unit exists
    unit = db.query(Unit).filter(Unit.id == reservation.unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    
    # Check if the guest exists
    guest = db.query(Guest).filter(Guest.id == reservation.guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    
    # Check for overlapping reservations
    if has_overlapping_reservation(db, reservation.unit_id, reservation.check_in_date, reservation.check_out_date):
        raise HTTPException(status_code=400, detail="Unit is already reserved for these dates")
    
    db_reservation = Reservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@app.get("/reservations/", response_model=List[ReservationResponse])
def read_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reservations = db.query(Reservation).offset(skip).limit(limit).all()
    return reservations 