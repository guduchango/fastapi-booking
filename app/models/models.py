from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Text, func
from sqlalchemy.orm import relationship
from app.database.database import Base

class Guest(Base):
    __tablename__ = "guests"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(50))
    reservations = relationship("Reservation", back_populates="guest")

class Unit(Base):
    __tablename__ = "units"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(Text)
    capacity = Column(Integer)
    is_available = Column(Boolean, default=True)
    reservations = relationship("Reservation", back_populates="unit")

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, ForeignKey("guests.id", ondelete="CASCADE"))
    unit_id = Column(Integer, ForeignKey("units.id", ondelete="CASCADE"))
    check_in_date = Column(Date, index=True)
    check_out_date = Column(Date, index=True)
    status = Column(String(50), default="active")
    created_at = Column(Date, server_default=func.current_date())
    
    guest = relationship("Guest", back_populates="reservations")
    unit = relationship("Unit", back_populates="reservations") 