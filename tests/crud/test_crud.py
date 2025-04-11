import pytest
from datetime import date
from app.crud import crud
from app.schemas import schemas

def test_create_guest(db_session, sample_guest_data):
    guest_data = schemas.GuestCreate(**sample_guest_data)
    guest = crud.create_guest(db=db_session, guest=guest_data)
    assert guest.name == sample_guest_data["name"]
    assert guest.email == sample_guest_data["email"]
    assert guest.phone == sample_guest_data["phone"]

def test_get_guests(db_session, sample_guest_data):
    guest_data = schemas.GuestCreate(**sample_guest_data)
    crud.create_guest(db=db_session, guest=guest_data)
    
    guests = crud.get_guests(db=db_session)
    assert len(guests) > 0
    assert guests[0].name == sample_guest_data["name"]

def test_create_unit(db_session, sample_unit_data):
    unit_data = schemas.UnitCreate(**sample_unit_data)
    unit = crud.create_unit(db=db_session, unit=unit_data)
    assert unit.name == sample_unit_data["name"]
    assert unit.description == sample_unit_data["description"]
    assert unit.capacity == sample_unit_data["capacity"]

def test_get_units(db_session, sample_unit_data):
    unit_data = schemas.UnitCreate(**sample_unit_data)
    crud.create_unit(db=db_session, unit=unit_data)
    
    units = crud.get_units(db=db_session)
    assert len(units) > 0
    assert units[0].name == sample_unit_data["name"]

def test_create_reservation(db_session, sample_reservation_data):
    reservation_data = schemas.ReservationCreate(**sample_reservation_data)
    reservation = crud.create_reservation(db=db_session, reservation=reservation_data)
    assert reservation.guest_id == sample_reservation_data["guest_id"]
    assert reservation.unit_id == sample_reservation_data["unit_id"]
    assert str(reservation.check_in_date) == sample_reservation_data["check_in_date"]
    assert str(reservation.check_out_date) == sample_reservation_data["check_out_date"]

def test_get_reservations(db_session, sample_reservation_data):
    reservation_data = schemas.ReservationCreate(**sample_reservation_data)
    crud.create_reservation(db=db_session, reservation=reservation_data)
    
    reservations = crud.get_reservations(db=db_session)
    assert len(reservations) > 0
    assert reservations[0].guest_id == sample_reservation_data["guest_id"]

def test_update_reservation(db_session, sample_reservation_data):
    # Primero creamos una reserva
    reservation_data = schemas.ReservationCreate(**sample_reservation_data)
    reservation = crud.create_reservation(db=db_session, reservation=reservation_data)
    
    # Actualizamos la reserva
    update_data = schemas.ReservationUpdate(
        check_in_date=date(2024, 4, 10),
        check_out_date=date(2024, 4, 15)
    )
    updated_reservation = crud.update_reservation(
        db=db_session,
        reservation_id=reservation.id,
        reservation_update=update_data
    )
    assert str(updated_reservation.check_in_date) == "2024-04-10"
    assert str(updated_reservation.check_out_date) == "2024-04-15"

def test_overlapping_reservation(db_session, sample_reservation_data):
    # Primero creamos una reserva
    reservation_data = schemas.ReservationCreate(**sample_reservation_data)
    crud.create_reservation(db=db_session, reservation=reservation_data)
    
    # Intentamos crear una reserva que se solapa
    overlapping_data = schemas.ReservationCreate(
        guest_id=sample_reservation_data["guest_id"],
        unit_id=sample_reservation_data["unit_id"],
        check_in_date=date(2024, 4, 3),  # Se solapa con la reserva anterior
        check_out_date=date(2024, 4, 7)
    )
    
    with pytest.raises(ValueError) as exc_info:
        crud.create_reservation(db=db_session, reservation=overlapping_data)
    assert "Unit is already reserved for these dates" in str(exc_info.value) 