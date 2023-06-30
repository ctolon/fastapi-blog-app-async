"""Celery settings."""

from celery import Celery
from time import time

celery_app = Celery("worker", broker="amqp://guest@blog-app-queue//")
#celery_app.conf.broker_url = CELERY_BROKER_URL
#celery_app.conf.result_backend = CELERY_RESULT_BACKEND

celery_app.autodiscover_tasks()

class BaseTaskWithRetry(celery_app.Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True
    
@celery_app.task(name="create_test_task")
def create_test_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

# @shared_task(bind=True, base=BaseTaskWithRetry)
# def task_process_notification(self):
#     raise Exception()

# Sentry DSN not set.
#celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
