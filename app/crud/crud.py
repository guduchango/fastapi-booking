from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.models import models
from app.schemas import schemas
from app.email.email_service import EmailService

# Guest CRUD operations
def create_guest(db: Session, guest: schemas.GuestCreate):
    db_guest = models.Guest(**guest.model_dump())
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest

def get_guests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Guest).offset(skip).limit(limit).all()

def get_guest(db: Session, guest_id: int):
    return db.query(models.Guest).filter(models.Guest.id == guest_id).first()

# Unit CRUD operations
def create_unit(db: Session, unit: schemas.UnitCreate):
    db_unit = models.Unit(**unit.model_dump())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

def get_units(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Unit).offset(skip).limit(limit).all()

def get_unit(db: Session, unit_id: int):
    return db.query(models.Unit).filter(models.Unit.id == unit_id).first()

# Reservation CRUD operations
def has_overlapping_reservation(db: Session, unit_id: int, check_in: date, check_out: date, exclude_reservation_id: Optional[int] = None):
    query = db.query(models.Reservation).filter(
        models.Reservation.unit_id == unit_id,
        models.Reservation.status == "active",
        # Check for any overlap in the date ranges
        models.Reservation.check_in_date <= check_out,
        models.Reservation.check_out_date >= check_in
    )
    
    if exclude_reservation_id:
        query = query.filter(models.Reservation.id != exclude_reservation_id)
    
    return query.first() is not None

def create_reservation(db: Session, reservation: schemas.ReservationCreate):
    # Check if the unit exists
    unit = db.query(models.Unit).filter(models.Unit.id == reservation.unit_id).first()
    if not unit:
        raise ValueError("Unit not found")
    
    # Check if the guest exists
    guest = db.query(models.Guest).filter(models.Guest.id == reservation.guest_id).first()
    if not guest:
        raise ValueError("Guest not found")
    
    # Check for overlapping reservations
    if has_overlapping_reservation(db, reservation.unit_id, reservation.check_in_date, reservation.check_out_date):
        raise ValueError("Unit is already reserved for these dates")
    
    db_reservation = models.Reservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_reservations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Reservation).offset(skip).limit(limit).all()

def get_reservation(db: Session, reservation_id: int):
    return db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

def update_reservation(db: Session, reservation_id: int, reservation_update: schemas.ReservationUpdate):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not db_reservation:
        raise ValueError("Reservation not found")
    
    # Get the values to update
    update_data = reservation_update.model_dump(exclude_unset=True)
    
    # If updating dates or unit, check for overlaps
    if any(key in update_data for key in ['check_in_date', 'check_out_date', 'unit_id']):
        unit_id = update_data.get('unit_id', db_reservation.unit_id)
        check_in = update_data.get('check_in_date', db_reservation.check_in_date)
        check_out = update_data.get('check_out_date', db_reservation.check_out_date)
        
        if has_overlapping_reservation(db, unit_id, check_in, check_out, reservation_id):
            raise ValueError("Unit is already reserved for these dates")
    
    # If updating guest_id, verify guest exists
    if 'guest_id' in update_data:
        guest = db.query(models.Guest).filter(models.Guest.id == update_data['guest_id']).first()
        if not guest:
            raise ValueError("Guest not found")
    
    # If updating unit_id, verify unit exists
    if 'unit_id' in update_data:
        unit = db.query(models.Unit).filter(models.Unit.id == update_data['unit_id']).first()
        if not unit:
            raise ValueError("Unit not found")
    
    # Update the reservation
    for key, value in update_data.items():
        setattr(db_reservation, key, value)
    
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def cancel_reservation(db: Session, reservation_id: int):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not db_reservation:
        raise ValueError("Reservation not found")
    
    # Cambiar el estado de la reservación a "cancelada"
    db_reservation.status = "cancelled"
    
    db.commit()
    db.refresh(db_reservation)
    
    # Enviar correo de confirmación
    email_service = EmailService()
    context = {
        "guest_name": db_reservation.guest.name,
        "unit_name": db_reservation.unit.name,
        "check_in_date": db_reservation.check_in_date,
        "check_out_date": db_reservation.check_out_date,
        "reservation_id": db_reservation.id
    }
    email_service.send_email(
        to_email=db_reservation.guest.email,
        subject="Reservation Cancelled",
        template_name="reservation_cancellation",
        context=context
    )
    
    return db_reservation 