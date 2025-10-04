from celery.schedules import crontab
from ..celery_app import celery_app
from ..db import SessionLocal
from .importer import full_import
from sqlalchemy.orm import Session

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=0, hour=3), task_full_refresh.s())

@celery_app.task(name="etl.task_full_refresh", queue="etl", autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def task_full_refresh():
    db: Session = SessionLocal()
    try:
        full_import(db)
    finally:
        db.close()
