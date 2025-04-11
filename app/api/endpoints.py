from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas import schemas
from app.crud import crud

router = APIRouter()

@router.post("/guests/", response_model=schemas.GuestResponse)
def create_guest(guest: schemas.GuestCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_guest(db=db, guest=guest)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/guests/", response_model=List[schemas.GuestResponse])
def read_guests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    guests = crud.get_guests(db, skip=skip, limit=limit)
    return guests

@router.post("/units/", response_model=schemas.UnitResponse)
def create_unit(unit: schemas.UnitCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_unit(db=db, unit=unit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/units/", response_model=List[schemas.UnitResponse])
def read_units(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    units = crud.get_units(db, skip=skip, limit=limit)
    return units

@router.post("/reservations/", response_model=schemas.ReservationResponse)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_reservation(db=db, reservation=reservation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reservations/", response_model=List[schemas.ReservationResponse])
def read_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reservations = crud.get_reservations(db, skip=skip, limit=limit)
    return reservations

@router.put("/reservations/{reservation_id}", response_model=schemas.ReservationResponse)
def update_reservation(reservation_id: int, reservation_update: schemas.ReservationUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_reservation(db=db, reservation_id=reservation_id, reservation_update=reservation_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 