import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.database import Base, get_db
from app.models import models

# Configuración de la base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_db):
    connection = test_db.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
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
        "capacity": 2
    }

@pytest.fixture
def sample_reservation_data(sample_guest_data, sample_unit_data, db_session):
    # Crear guest y unit primero
    guest = models.Guest(**sample_guest_data)
    unit = models.Unit(**sample_unit_data)
    db_session.add(guest)
    db_session.add(unit)
    db_session.commit()
    db_session.refresh(guest)
    db_session.refresh(unit)
    
    return {
        "guest_id": guest.id,
        "unit_id": unit.id,
        "check_in_date": "2024-04-01",
        "check_out_date": "2024-04-05"
    } 