import pytest
from datetime import date, timedelta

def test_create_guest(client, sample_guest_data):
    response = client.post("/api/v1/guests/", json=sample_guest_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_guest_data["name"]
    assert data["email"] == sample_guest_data["email"]
    assert data["phone"] == sample_guest_data["phone"]

def test_get_guests(client, sample_guest_data):
    # Primero creamos un guest
    client.post("/api/v1/guests/", json=sample_guest_data)
    
    response = client.get("/api/v1/guests/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == sample_guest_data["name"]

def test_create_unit(client, sample_unit_data):
    response = client.post("/api/v1/units/", json=sample_unit_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_unit_data["name"]
    assert data["description"] == sample_unit_data["description"]
    assert data["capacity"] == sample_unit_data["capacity"]

def test_get_units(client, sample_unit_data):
    # Primero creamos una unit
    client.post("/api/v1/units/", json=sample_unit_data)
    
    response = client.get("/api/v1/units/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == sample_unit_data["name"]

def test_create_reservation(client, sample_reservation_data):
    response = client.post("/api/v1/reservations/", json=sample_reservation_data)
    assert response.status_code == 200
    data = response.json()
    assert data["guest_id"] == sample_reservation_data["guest_id"]
    assert data["unit_id"] == sample_reservation_data["unit_id"]
    assert data["check_in_date"] == sample_reservation_data["check_in_date"]
    assert data["check_out_date"] == sample_reservation_data["check_out_date"]

def test_get_reservations(client, sample_reservation_data):
    # Primero creamos una reserva
    client.post("/api/v1/reservations/", json=sample_reservation_data)
    
    response = client.get("/api/v1/reservations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["guest_id"] == sample_reservation_data["guest_id"]

def test_update_reservation(client, sample_reservation_data):
    # Primero creamos una reserva
    response = client.post("/api/v1/reservations/", json=sample_reservation_data)
    reservation_id = response.json()["id"]
    
    # Actualizamos la reserva
    update_data = {
        "check_in_date": "2024-04-10",
        "check_out_date": "2024-04-15"
    }
    response = client.put(f"/api/v1/reservations/{reservation_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["check_in_date"] == update_data["check_in_date"]
    assert data["check_out_date"] == update_data["check_out_date"]

def test_overlapping_reservation(client, sample_reservation_data):
    # Primero creamos una reserva
    client.post("/api/v1/reservations/", json=sample_reservation_data)
    
    # Intentamos crear una reserva que se solapa
    overlapping_data = {
        "guest_id": sample_reservation_data["guest_id"],
        "unit_id": sample_reservation_data["unit_id"],
        "check_in_date": "2024-04-03",  # Se solapa con la reserva anterior
        "check_out_date": "2024-04-07"
    }
    response = client.post("/api/v1/reservations/", json=overlapping_data)
    assert response.status_code == 400
    assert "Unit is already reserved for these dates" in response.json()["detail"] 