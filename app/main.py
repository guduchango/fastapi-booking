from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.database.database import engine, Base
from app.email.email_service import EmailService
from app.worker import celery_app
from app.metrics import metrics_middleware, start_metrics_server
import os

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

# Add metrics middleware
app.middleware("http")(metrics_middleware)

# Include API routes
app.include_router(router, prefix="/api/v1")

# Initialize email service
email_service = EmailService()

# Start metrics server only if not in test mode
if not os.getenv("TESTING"):
    start_metrics_server(port=int(os.getenv("METRICS_PORT", "8001")))

@app.get("/")
async def root():
    return {"message": "Welcome to the Reservation System API"} 