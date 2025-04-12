import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from app.main import app
from app.database.database import Base, get_db
from app.models import models
from app.models.models import Guest, Unit, Reservation
from datetime import datetime, timedelta

# Use test database
SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin123@postgres:5432/reservations_test"

# Create test engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database tables
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    # Clean up all tables before each test
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_guest_data():
    return {
        "name": "Test Guest",
        "email": "test@example.com",
        "phone": "1234567890"
    }

@pytest.fixture
def sample_unit_data():
    return {
        "name": "Test Unit",
        "description": "Test Description",
        "capacity": 2,
        "is_available": True
    }

@pytest.fixture
def sample_reservation_data(db_session, sample_guest_data, sample_unit_data):
    # Create guest
    guest = Guest(**sample_guest_data)
    db_session.add(guest)
    db_session.commit()
    db_session.refresh(guest)
    
    # Create unit
    unit = Unit(**sample_unit_data)
    db_session.add(unit)
    db_session.commit()
    db_session.refresh(unit)
    
    return {
        "guest_id": guest.id,
        "unit_id": unit.id,
        "check_in_date": "2024-04-01",
        "check_out_date": "2024-04-05",
        "status": "pending"
    } 