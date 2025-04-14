from locust import HttpUser, task, between
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import logging
import os

# Configurar logging
log_dir = "/locust/logs"
os.makedirs(log_dir, exist_ok=True)

# Configurar el logger para escribir en archivo y consola
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_dir}/locust_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ReservationUser(HttpUser):
    host = "http://app:8000"  # Cambiado para usar el nombre del servicio en docker-compose
    wait_time = between(1, 3)

    def on_start(self):
        """Inicializa los datos necesarios para las pruebas"""
        logger.info("Iniciando usuario de prueba")
        self.guest_ids = []
        self.unit_ids = []
        self.reservations: Dict[int, List[Tuple[str, str, int]]] = {}  # unit_id: [(check_in, check_out, guest_id)]
        self.current_unit_index = 0  # Para llevar el control de la unidad actual
        self.initialize_data()

    def initialize_data(self):
        """Crea las unidades y huéspedes iniciales"""
        logger.info("Iniciando creación de unidades y huéspedes")
        # Crear 20 unidades
        for i in range(1, 21):
            unit_num = i
            payload = {
                "name": f"Unit {unit_num}",
                "description": f"Test unit {unit_num}",
                "capacity": random.randint(2, 6),
                "price_per_night": random.uniform(100.0, 500.0)
            }
            logger.info(f"Creando unidad {unit_num} con payload: {payload}")
            try:
                response = self.client.post("/api/v1/units/", json=payload)
                if response.status_code == 200:
                    unit_data = response.json()
                    self.unit_ids.append(unit_data["id"])
                    self.reservations[unit_data["id"]] = []
                    logger.info(f"Unidad {unit_num} creada exitosamente con ID: {unit_data['id']}")
                else:
                    logger.error(f"Error al crear unidad {unit_num}: {response.status_code} - {response.text}")
            except Exception as e:
                logger.error(f"Error de conexión al crear unidad {unit_num}: {str(e)}")

        # Crear 100 huéspedes
        for i in range(1, 101):
            guest_num = i
            payload = {
                "name": f"Guest {guest_num}",
                "email": f"guest{guest_num}@example.com",
                "phone": f"{guest_num}555{guest_num}"
            }
            logger.info(f"Creando huésped {guest_num} con payload: {payload}")
            try:
                response = self.client.post("/api/v1/guests/", json=payload)
                if response.status_code == 200:
                    guest_data = response.json()
                    self.guest_ids.append(guest_data["id"])
                    logger.info(f"Huésped {guest_num} creado exitosamente con ID: {guest_data['id']}")
                else:
                    logger.error(f"Error al crear huésped {guest_num}: {response.status_code} - {response.text}")
            except Exception as e:
                logger.error(f"Error de conexión al crear huésped {guest_num}: {str(e)}")

    def get_next_dates(self, base_date: datetime) -> Tuple[str, str]:
        """Genera las fechas de check-in y check-out para la siguiente reserva"""
        check_in = base_date + timedelta(days=1)
        check_out = check_in + timedelta(days=3)
        return check_in.strftime("%Y-%m-%d"), check_out.strftime("%Y-%m-%d")

    @task(1)
    def create_reservations(self):
        """Crea reservas secuenciales para cada unidad"""
        if not self.guest_ids or not self.unit_ids:
            logger.warning("No hay huéspedes o unidades disponibles para crear reservas")
            return

        # Fecha base para comenzar las reservas
        current_date = datetime.now()
        end_date = current_date + timedelta(days=150)  # 5 meses aproximadamente
        logger.info(f"Iniciando creación de reservas desde {current_date} hasta {end_date}")

        while current_date < end_date:
            # Obtener la unidad actual
            current_unit_id = self.unit_ids[self.current_unit_index]
            
            # Obtener un huésped aleatorio
            guest_id = random.choice(self.guest_ids)
            
            # Generar fechas para la reserva
            check_in, check_out = self.get_next_dates(current_date)
            
            # Crear la reserva
            payload = {
                "guest_id": guest_id,
                "unit_id": current_unit_id,
                "check_in_date": check_in,
                "check_out_date": check_out,
                "adults": random.randint(1, 4),
                "children": random.randint(0, 3)
            }
            
            logger.info(f"Intentando crear reserva: Unidad {current_unit_id}, Huésped {guest_id}, Fechas {check_in} - {check_out}")
            
            try:
                response = self.client.post("/api/v1/reservations/", json=payload)
                
                if response.status_code == 200:
                    # Registrar la reserva
                    if current_unit_id not in self.reservations:
                        self.reservations[current_unit_id] = []
                    self.reservations[current_unit_id].append((check_in, check_out, guest_id))
                    logger.info(f"Reserva creada exitosamente: Unidad {current_unit_id}, Huésped {guest_id}")
                    
                    # Avanzar al siguiente día
                    current_date = datetime.strptime(check_out, "%Y-%m-%d")
                    
                    # Avanzar a la siguiente unidad
                    self.current_unit_index = (self.current_unit_index + 1) % len(self.unit_ids)
                else:
                    logger.error(f"Error al crear reserva: {response.status_code} - {response.text}")
                    # Si hay un error, avanzar al siguiente día de todos modos
                    current_date = current_date + timedelta(days=1)
            except Exception as e:
                logger.error(f"Error de conexión al crear reserva: {str(e)}")
                current_date = current_date + timedelta(days=1)


    @task(1)
    def get_reservation(self):
        """Obtiene una reserva existente"""
        if not self.reservations:
            logger.warning("No hay reservas disponibles para consultar")
            return

        # Seleccionar una unidad aleatoria que tenga reservas
        unit_id = random.choice(list(self.reservations.keys()))
        if not self.reservations[unit_id]:
            return

        # Seleccionar una reserva aleatoria de la unidad
        reservation = random.choice(self.reservations[unit_id])
        check_in, check_out, guest_id = reservation

        logger.info(f"Consultando reserva: Unidad {unit_id}, Fechas {check_in} - {check_out}")
        try:
            response = self.client.get(f"/api/v1/reservations/{unit_id}")
            if response.status_code == 200:
                logger.info(f"Reserva consultada exitosamente: {response.json()}")
            else:
                logger.error(f"Error al consultar reserva: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error de conexión al consultar reserva: {str(e)}")



# Asegurarse de que la clase esté disponible para Locust
__all__ = ['ReservationUser']
