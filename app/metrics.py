from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
from typing import Dict, Any

# API Metrics
REQUEST_COUNT = Counter(
    'reservation_api_requests_total',
    'Total number of API requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'reservation_api_request_latency_seconds',
    'API request latency in seconds',
    ['method', 'endpoint']
)

# Cache Metrics
CACHE_HITS = Counter(
    'reservation_cache_hits_total',
    'Total number of cache hits',
    ['cache_type']
)

CACHE_MISSES = Counter(
    'reservation_cache_misses_total',
    'Total number of cache misses',
    ['cache_type']
)

# Database Metrics
DB_QUERY_TIME = Histogram(
    'reservation_db_query_time_seconds',
    'Database query execution time',
    ['query_type']
)

DB_CONNECTIONS = Gauge(
    'reservation_db_connections',
    'Number of active database connections'
)

# Email Metrics
EMAIL_SENT = Counter(
    'reservation_emails_sent_total',
    'Total number of emails sent',
    ['email_type', 'status']
)

EMAIL_ERRORS = Counter(
    'reservation_email_errors_total',
    'Total number of email sending errors',
    ['error_type']
)

# Celery Metrics
CELERY_TASKS = Counter(
    'reservation_celery_tasks_total',
    'Total number of Celery tasks',
    ['task_name', 'status']
)

CELERY_TASK_TIME = Histogram(
    'reservation_celery_task_time_seconds',
    'Celery task execution time',
    ['task_name']
)

# Start metrics server
def start_metrics_server(port: int = 8001):
    start_http_server(port)

# Middleware to track requests
async def metrics_middleware(request, call_next):
    start_time = time.time()
    method = request.method
    endpoint = request.url.path
    
    try:
        response = await call_next(request)
        status_code = response.status_code
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status_code).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - start_time)
        return response
    except Exception as e:
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=500).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - start_time)
        raise e 