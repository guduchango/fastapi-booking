from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.database.database import engine, Base
from app.email.email_service import EmailService
from app.worker import celery_app
from app.metrics import metrics_middleware
import os
from prometheus_client import make_asgi_app
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Error creating database tables: {str(e)}")

# Create FastAPI app
app = FastAPI(
    title="Reservation System API",
    description="API for managing reservations, guests, and units",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar middleware de métricas
app.middleware("http")(metrics_middleware)

# Agregar endpoint de métricas
@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Include API routes
app.include_router(router, prefix="/api/v1")

# Initialize email service
email_service = EmailService()

@app.get("/")
async def root():
    return {"message": "Welcome to the Reservation System API"} 