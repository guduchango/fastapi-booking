from locust import HttpUser, task, between
import random
from datetime import datetime, timedelta
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReservationUser(HttpUser):
    wait_time = between(1, 3)  # Espera entre 1 y 3 segundos entre tareas
    
    def on_start(self):
        """Se ejecuta cuando un usuario inicia."""
        self.client.headers = {"Content-Type": "application/json"}
        # Obtener IDs válidos al inicio
        self.valid_guest_ids = self._get_valid_guest_ids()
        self.valid_unit_ids = self._get_valid_unit_ids()
        logger.info(f"IDs válidos cargados - Guests: {len(self.valid_guest_ids)}, Units: {len(self.valid_unit_ids)}")
    
    def _get_valid_guest_ids(self):
        """Obtener IDs de huéspedes válidos."""
        try:
            response = self.client.get("/api/v1/guests/")
            if response.status_code == 200:
                guests = response.json()
                return [guest["id"] for guest in guests]
            return []
        except Exception as e:
            logger.error(f"Error obteniendo guest IDs: {e}")
            return []
    
    def _get_valid_unit_ids(self):
        """Obtener IDs de unidades válidas."""
        try:
            response = self.client.get("/api/v1/units/")
            if response.status_code == 200:
                units = response.json()
                return [unit["id"] for unit in units if unit.get("is_available", True)]
            return []
        except Exception as e:
            logger.error(f"Error obteniendo unit IDs: {e}")
            return []
    
    def _generate_valid_dates(self):
        """Generar fechas válidas para una reserva."""
        today = datetime.now().date()
        # Check-in entre 1 y 30 días en el futuro
        check_in = today + timedelta(days=random.randint(1, 30))
        # Check-out entre 1 y 7 días después del check-in
        check_out = check_in + timedelta(days=random.randint(1, 7))
        return check_in, check_out
    
    @task(3)
    def list_reservations(self):
        """Listar reservas (tarea más frecuente)."""
        self.client.get("/api/v1/reservations/")
    
    @task(1)
    def create_reservation(self):
        """Crear una nueva reserva."""
        if not self.valid_guest_ids or not self.valid_unit_ids:
            logger.warning("No hay IDs válidos disponibles")
            return
        
        # Seleccionar IDs aleatorios de las listas válidas
        guest_id = random.choice(self.valid_guest_ids)
        unit_id = random.choice(self.valid_unit_ids)
        
        # Generar fechas válidas
        check_in, check_out = self._generate_valid_dates()
        
        # Datos de la reserva
        reservation_data = {
            "guest_id": guest_id,
            "unit_id": unit_id,
            "check_in_date": check_in.strftime("%Y-%m-%d"),
            "check_out_date": check_out.strftime("%Y-%m-%d")
        }
        
        try:
            response = self.client.post("/api/v1/reservations/", json=reservation_data)
            if response.status_code == 201:
                logger.info(f"Reserva creada exitosamente: {response.json()}")
            else:
                logger.error(f"Error creando reserva: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Excepción creando reserva: {e}")
    
    @task(2)
    def get_reservation(self):
        """Obtener una reserva específica."""
        try:
            # Primero obtener la lista de reservas
            response = self.client.get("/api/v1/reservations/")
            if response.status_code == 200:
                reservations = response.json()
                if reservations:
                    # Seleccionar una reserva aleatoria
                    reservation = random.choice(reservations)
                    reservation_id = reservation["id"]
                    # Obtener los detalles de la reserva
                    self.client.get(f"/api/v1/reservations/{reservation_id}")
        except Exception as e:
            logger.error(f"Error obteniendo reserva: {e}")
    
    @task(1)
    def update_reservation(self):
        """Actualizar una reserva existente."""
        try:
            # Primero obtener la lista de reservas
            response = self.client.get("/api/v1/reservations/")
            if response.status_code == 200:
                reservations = response.json()
                if reservations:
                    # Seleccionar una reserva aleatoria
                    reservation = random.choice(reservations)
                    reservation_id = reservation["id"]
                    
                    # Generar nuevas fechas válidas
                    check_in, check_out = self._generate_valid_dates()
                    
                    update_data = {
                        "check_in_date": check_in.strftime("%Y-%m-%d"),
                        "check_out_date": check_out.strftime("%Y-%m-%d")
                    }
                    
                    # Actualizar la reserva
                    response = self.client.put(
                        f"/api/v1/reservations/{reservation_id}", 
                        json=update_data
                    )
                    if response.status_code == 200:
                        logger.info(f"Reserva actualizada exitosamente: {response.json()}")
                    else:
                        logger.error(f"Error actualizando reserva: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error actualizando reserva: {e}") 