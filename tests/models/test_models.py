import pytest
from datetime import date
from app.models import models

def test_guest_model(db_session):
    guest = models.Guest(
        name="Test Guest",
        email="test@example.com",
        phone="1234567890"
    )
    db_session.add(guest)
    db_session.commit()
    db_session.refresh(guest)
    
    assert guest.id is not None
    assert guest.name == "Test Guest"
    assert guest.email == "test@example.com"
    assert guest.phone == "1234567890"

def test_unit_model(db_session):
    unit = models.Unit(
        name="Test Unit",
        description="Test Description",
        capacity=2
    )
    db_session.add(unit)
    db_session.commit()
    db_session.refresh(unit)
    
    assert unit.id is not None
    assert unit.name == "Test Unit"
    assert unit.description == "Test Description"
    assert unit.capacity == 2

def test_reservation_model(db_session):
    # Primero creamos un guest y una unit
    guest = models.Guest(
        name="Test Guest",
        email="test@example.com",
        phone="1234567890"
    )
    unit = models.Unit(
        name="Test Unit",
        description="Test Description",
        capacity=2
    )
    db_session.add(guest)
    db_session.add(unit)
    db_session.commit()
    db_session.refresh(guest)
    db_session.refresh(unit)
    
    # Creamos la reserva
    reservation = models.Reservation(
        guest_id=guest.id,
        unit_id=unit.id,
        check_in_date=date(2024, 4, 1),
        check_out_date=date(2024, 4, 5)
    )
    db_session.add(reservation)
    db_session.commit()
    db_session.refresh(reservation)
    
    assert reservation.id is not None
    assert reservation.guest_id == guest.id
    assert reservation.unit_id == unit.id
    assert str(reservation.check_in_date) == "2024-04-01"
    assert str(reservation.check_out_date) == "2024-04-05"
    assert reservation.status == "active"

def test_reservation_relationships(db_session):
    # Creamos un guest y una unit
    guest = models.Guest(
        name="Test Guest",
        email="test@example.com",
        phone="1234567890"
    )
    unit = models.Unit(
        name="Test Unit",
        description="Test Description",
        capacity=2
    )
    db_session.add(guest)
    db_session.add(unit)
    db_session.commit()
    db_session.refresh(guest)
    db_session.refresh(unit)
    
    # Creamos una reserva
    reservation = models.Reservation(
        guest_id=guest.id,
        unit_id=unit.id,
        check_in_date=date(2024, 4, 1),
        check_out_date=date(2024, 4, 5)
    )
    db_session.add(reservation)
    db_session.commit()
    db_session.refresh(reservation)
    
    # Verificamos las relaciones
    assert reservation.guest == guest
    assert reservation.unit == unit
    assert reservation in guest.reservations
    assert reservation in unit.reservations 