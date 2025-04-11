# Reservation System with FastAPI

This is a reservation system developed with FastAPI that handles guests, units, and reservations.

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
python run.py run
```

## API Endpoints

### Guests

- `POST /api/v1/guests/` - Create a new guest
- `GET /api/v1/guests/` - List all guests

### Units

- `POST /api/v1/units/` - Create a new unit
- `GET /api/v1/units/` - List all units

### Reservations

- `POST /api/v1/reservations/` - Create a new reservation
- `GET /api/v1/reservations/` - List all reservations
- `PUT /api/v1/reservations/{reservation_id}` - Update a reservation

## Validations

The system includes the following validations:

1. Cannot create reservations for non-existent units
2. Cannot create reservations for non-existent guests
3. Cannot create overlapping reservations for the same unit

## Example Usage

### Create a guest
```json
POST /api/v1/guests/
{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890"
}
```

### Create a unit
```json
POST /api/v1/units/
{
    "name": "Suite 101",
    "description": "Luxury suite with sea view",
    "capacity": 2
}
```

### Create a reservation
```json
POST /api/v1/reservations/
{
    "guest_id": 1,
    "unit_id": 1,
    "check_in_date": "2024-04-15",
    "check_out_date": "2024-04-20"
}
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

To run the tests:
```bash
pytest
```

## Populating the Database

To populate the database with sample data:
```bash
python run.py seed 