from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine
from app.models.models import Guest, Unit, Reservation
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker()

def create_fake_guests(db: Session, count: int = 10):
    """Create fake guests."""
    for _ in range(count):
        guest = Guest(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number()
        )
        db.add(guest)
    db.commit()

def create_fake_units(db: Session, count: int = 5):
    """Create fake units."""
    unit_types = [
        ("Presidential Suite", "Luxurious suite with ocean view", 4),
        ("Executive Suite", "Modern suite with city view", 2),
        ("Family Room", "Spacious room for families", 6),
        ("Standard Room", "Comfortable room with basic amenities", 2),
        ("Deluxe Room", "Upgraded room with premium amenities", 2)
    ]
    
    for name, description, capacity in unit_types:
        unit = Unit(
            name=name,
            description=description,
            capacity=capacity,
            is_available=True
        )
        db.add(unit)
    db.commit()

def create_fake_reservations(db: Session, count: int = 15):
    """Create fake reservations."""
    guests = db.query(Guest).all()
    units = db.query(Unit).all()
    
    for _ in range(count):
        guest = random.choice(guests)
        unit = random.choice(units)
        
        # Generate random dates within the next month
        today = date.today()
        check_in = today + timedelta(days=random.randint(1, 15))
        check_out = check_in + timedelta(days=random.randint(1, 7))
        
        # Check for overlapping reservations
        overlapping = db.query(Reservation).filter(
            Reservation.unit_id == unit.id,
            Reservation.check_in_date < check_out,
            Reservation.check_out_date > check_in
        ).first()
        
        if not overlapping:
            reservation = Reservation(
                guest_id=guest.id,
                unit_id=unit.id,
                check_in_date=check_in,
                check_out_date=check_out,
                status="active"
            )
            db.add(reservation)
    
    db.commit()

def seed_database():
    """Seed the database with initial data."""
    db = SessionLocal()
    try:
        # Create tables if they don't exist
        from app.models.models import Base
        Base.metadata.create_all(bind=engine)
        
        # Check if we already have data
        if db.query(Guest).count() == 0:
            create_fake_guests(db)
            print("Created fake guests")
        
        if db.query(Unit).count() == 0:
            create_fake_units(db)
            print("Created fake units")
        
        if db.query(Reservation).count() == 0:
            create_fake_reservations(db)
            print("Created fake reservations")
        
        print("Database seeded successfully")
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database() 