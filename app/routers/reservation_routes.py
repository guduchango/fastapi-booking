from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models import models
from app.schemas import schemas
from app.utils.errors import (
    UnitNotFoundError,
    GuestNotFoundError,
    OverlappingReservationError,
    DatabaseError
)
from app.utils.cache import cached, invalidate_cache
from app.crud import crud

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.post("/", response_model=schemas.ReservationResponse)
@invalidate_cache("reservation")
async def create_reservation(
    reservation: schemas.ReservationCreate,
    db: Session = Depends(get_db)
) -> schemas.ReservationResponse:
    """Create a new reservation."""
    try:
        # Check if the unit exists
        unit = crud.get_unit(db=db, unit_id=reservation.unit_id)
        if not unit:
            raise UnitNotFoundError(reservation.unit_id)
        
        # Check if the guest exists
        guest = crud.get_guest(db=db, guest_id=reservation.guest_id)
        if not guest:
            raise GuestNotFoundError(reservation.guest_id)
        
        # Check for overlapping reservations
        if crud.has_overlapping_reservation(
            db=db,
            unit_id=reservation.unit_id,
            check_in=reservation.check_in_date,
            check_out=reservation.check_out_date
        ):
            raise OverlappingReservationError(reservation.unit_id)
        
        # Create the reservation
        db_reservation = crud.create_reservation(db=db, reservation=reservation)
        return db_reservation
        
    except Exception as e:
        raise DatabaseError(str(e))

@router.get("/", response_model=List[schemas.ReservationResponse])
@cached(ttl=60)
async def read_reservations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[schemas.ReservationResponse]:
    """Get a list of reservations."""
    try:
        return crud.get_reservations(db=db, skip=skip, limit=limit)
    except Exception as e:
        raise DatabaseError(str(e))

@router.get("/{reservation_id}", response_model=schemas.ReservationResponse)
@cached(ttl=60)
async def read_reservation(
    reservation_id: int,
    db: Session = Depends(get_db)
) -> schemas.ReservationResponse:
    """Get a specific reservation by ID."""
    try:
        reservation = crud.get_reservation(db=db, reservation_id=reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")
        return reservation
    except Exception as e:
        raise DatabaseError(str(e))

@router.put("/{reservation_id}", response_model=schemas.ReservationResponse)
@invalidate_cache("reservation")
async def update_reservation(
    reservation_id: int,
    reservation_update: schemas.ReservationUpdate,
    db: Session = Depends(get_db)
) -> schemas.ReservationResponse:
    """Update a reservation."""
    try:
        return crud.update_reservation(
            db=db,
            reservation_id=reservation_id,
            reservation_update=reservation_update
        )
    except ValueError as e:
        raise DatabaseError(str(e))
    except Exception as e:
        raise DatabaseError(str(e)) 