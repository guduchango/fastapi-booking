from faker import Faker
from datetime import date, timedelta
import random
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models import models
from app.crud import crud
from app.schemas import schemas

fake = Faker('en_US')  # Using English for data

def create_fake_guests(db: Session, count: int = 10):
    guests = []
    for _ in range(count):
        guest_data = schemas.GuestCreate(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number()
        )
        guest = crud.create_guest(db=db, guest=guest_data)
        guests.append(guest)
    return guests

def create_fake_units(db: Session, count: int = 5):
    units = []
    unit_types = [
        ("Presidential Suite", "Luxury suite with sea view and jacuzzi", 2),
        ("Executive Suite", "Suite with living room and panoramic view", 2),
        ("Deluxe Room", "Spacious room with balcony", 2),
        ("Standard Room", "Comfortable room with all amenities", 2),
        ("Family Room", "Spacious room for 4 people", 4)
    ]
    
    for i in range(min(count, len(unit_types))):
        name, description, capacity = unit_types[i]
        unit_data = schemas.UnitCreate(
            name=f"{name} {i+1}",
            description=description,
            capacity=capacity
        )
        unit = crud.create_unit(db=db, unit=unit_data)
        units.append(unit)
    return units

def create_fake_reservations(db: Session, guests: list, units: list, count: int = 15):
    reservations = []
    today = date.today()
    
    for _ in range(count):
        # Select random guest and unit
        guest = random.choice(guests)
        unit = random.choice(units)
        
        # Generate random dates
        check_in = today + timedelta(days=random.randint(0, 30))
        check_out = check_in + timedelta(days=random.randint(1, 7))
        
        try:
            reservation_data = schemas.ReservationCreate(
                guest_id=guest.id,
                unit_id=unit.id,
                check_in_date=check_in,
                check_out_date=check_out
            )
            reservation = crud.create_reservation(db=db, reservation=reservation_data)
            reservations.append(reservation)
        except ValueError:
            # If there's a date conflict, try with other dates
            continue
    
    return reservations

def seed_database():
    db = SessionLocal()
    try:
        # Create test data
        print("Creating guests...")
        guests = create_fake_guests(db)
        print(f"Created {len(guests)} guests")
        
        print("Creating units...")
        units = create_fake_units(db)
        print(f"Created {len(units)} units")
        
        print("Creating reservations...")
        reservations = create_fake_reservations(db, guests, units)
        print(f"Created {len(reservations)} reservations")
        
        db.commit()
        print("Database populated successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error populating database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database() 