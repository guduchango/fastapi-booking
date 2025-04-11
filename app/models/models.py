from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

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