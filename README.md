# Reservation System API

A FastAPI-based reservation system with PostgreSQL, Redis, RabbitMQ, and monitoring tools.

## Features

- RESTful API for managing reservations, guests, and units
- PostgreSQL database with SQLAlchemy ORM
- Redis for caching and Celery broker
- RabbitMQ for message queuing
- Email notifications using Celery tasks
- Monitoring with Prometheus and Grafana
- Error tracking with Sentry
- Distributed tracing with OpenTelemetry
- Database management with pgAdmin
- Email testing with Mailhog

## Prerequisites

- Docker and Docker Compose
- Python 3.12 or higher
- Git

## Project Structure

```
.
├── app/
│   ├── api/              # API endpoints
│   ├── crud/             # Database operations
│   ├── database/         # Database configuration
│   ├── email/            # Email service and templates
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic models
│   ├── seeds/            # Database seeding
│   └── worker.py         # Celery worker configuration
├── prometheus/           # Prometheus configuration
├── docker-compose.yml    # Docker services configuration
├── Dockerfile            # Application container
├── Dockerfile.worker     # Celery worker container
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Build and start the services:
```bash
# Build the Docker images
docker-compose build

# Start all services
docker-compose up -d
```

This will start the following services:
- FastAPI application (http://localhost:8000)
- PostgreSQL database (port 5432)
- pgAdmin (http://localhost:5050)
- Redis (port 6379)
- RabbitMQ (http://localhost:15672)
- Mailhog (http://localhost:8025)
- Prometheus (http://localhost:9090)
- Grafana (http://localhost:3000)
- Sentry (http://localhost:9000)
- Celery worker
- Celery Flower (http://localhost:5555)

3. Seed the database with initial data:
```bash
# Access the application container
docker exec -it reservation-api /bin/bash

# Inside the container, run the seeding script
python -m app.seeds.seed_data

# Exit the container
exit
```

4. Set up the Python environment and install dependencies (for local development):
```bash
# Create a virtual environment
python -m venv env

# Activate the virtual environment
# On Linux/Mac:
source env/bin/activate
# On Windows:
# env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Accessing the Application Container

To access the application container and run Python commands:

1. Find the container ID:
```bash
docker ps
```

2. Access the container:
```bash
docker exec -it <container_id> /bin/bash
```

3. Once inside the container, you can:
   - Run Python commands:
     ```bash
     python
     ```
   - Run the application directly:
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port 8000
     ```
   - Run the Celery worker:
     ```bash
     celery -A app.worker worker --loglevel=info
     ```
   - Run database migrations:
     ```bash
     python -m alembic upgrade head
     ```
   - Run tests:
     ```bash
     pytest
     ```

4. To exit the container:
```bash
exit
```

## API Documentation

Once the services are running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints

- `POST /api/v1/guests/` - Create a new guest
- `GET /api/v1/guests/` - List all guests
- `POST /api/v1/units/` - Create a new unit
- `GET /api/v1/units/` - List all units
- `POST /api/v1/reservations/` - Create a new reservation
- `GET /api/v1/reservations/` - List all reservations
- `PUT /api/v1/reservations/{reservation_id}` - Update a reservation

## Monitoring and Management

### Database Management
- pgAdmin: http://localhost:5050
  - Email: admin@admin.com
  - Password: admin
  - Server: postgres:5432
  - Database: reservations
  - Username: admin
  - Password: admin

### Email Testing
- Mailhog: http://localhost:8025
  - SMTP: localhost:1025

### Message Queue
- RabbitMQ Management: http://localhost:15672
  - Username: admin
  - Password: admin

### Task Monitoring
- Celery Flower: http://localhost:5555

### Metrics and Monitoring
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
  - Username: admin
  - Password: admin

### Error Tracking
- Sentry: http://localhost:9000

## Development

1. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

4. Run the Celery worker:
```bash
celery -A app.worker worker --loglevel=info
```

## Testing

Run the test suite:
```bash
pytest
```

## Environment Variables

The following environment variables can be configured:

- `DATABASE_URL`: PostgreSQL connection string
- `CELERY_BROKER_URL`: RabbitMQ connection string
- `CELERY_RESULT_BACKEND`: Redis connection string
- `SMTP_HOST`: Mailhog host
- `SMTP_PORT`: Mailhog port
- `FROM_EMAIL`: Sender email address

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.