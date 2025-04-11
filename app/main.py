from fastapi import FastAPI
from app.api.endpoints import router
from app.database.database import engine
from app.models import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Reservation System",
    description="API for managing unit reservations",
    version="1.0.0"
)

# Include the router
app.include_router(router, prefix="/api/v1") 