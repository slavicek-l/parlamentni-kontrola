from celery import Celery
from .config import settings

celery_app = Celery("parlamentnikontrola",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)
celery_app.conf.task_default_queue = "default"
celery_app.conf.result_expires = 3600
celery_app.conf.worker_max_tasks_per_child = 100
celery_app.conf.beat_schedule = {}
