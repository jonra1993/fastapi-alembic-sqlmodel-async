# Celery is good for data-intensive application or some long-running tasks in other simple cases use Fastapi background tasks
from celery import Celery
from app.core.config import settings

celery = Celery(
    "async_task", broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
)

class CeleryConfig:
    task_serializer = "pickle"
    result_serializer = "pickle"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]

#celery.config_from_object(CeleryConfig)

celery.conf.result_backend = settings.SYNC_CELERY_DATABASE_URI
celery.conf.update({"beat_dburi": settings.SYNC_CELERY_BEAT_DATABASE_URI})
celery.autodiscover_tasks()

from app.api.celery_task import *
