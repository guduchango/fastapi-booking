from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class ReservationError(HTTPException):
    """Base class for reservation-related errors."""
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class UnitNotFoundError(ReservationError):
    """Raised when a unit is not found."""
    def __init__(self, unit_id: int) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unit with id {unit_id} not found"
        )

class GuestNotFoundError(ReservationError):
    """Raised when a guest is not found."""
    def __init__(self, guest_id: int) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guest with id {guest_id} not found"
        )

class OverlappingReservationError(ReservationError):
    """Raised when there's an overlapping reservation."""
    def __init__(self, unit_id: int) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unit {unit_id} is already reserved for these dates"
        )

class DatabaseError(ReservationError):
    """Raised when there's a database error."""
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {detail}"
        ) 