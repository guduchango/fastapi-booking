from celery import Celery
from app.email.email_service import EmailService
import os
import asyncio

# Initialize Celery
celery_app = Celery(
    'reservations',
    broker=os.getenv('CELERY_BROKER_URL', 'amqp://admin:admin@rabbitmq:5672//'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Initialize email service
email_service = EmailService()

@celery_app.task(name='send_reservation_email')
def send_reservation_email_task(email_data: dict):
    """Task to send reservation confirmation email."""
    try:
        # Create a new event loop for the async operation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run the async function in the event loop
        result = loop.run_until_complete(
            email_service.send_email(
                to_email=email_data['to_email'],
                subject=email_data['subject'],
                template_name=email_data['template_name'],
                context=email_data['context']
            )
        )
        
        # Close the event loop
        loop.close()
        
        return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)} 