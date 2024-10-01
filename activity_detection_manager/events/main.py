
from events.config.celery_utils import create_celery
from events.tasks.fetch_api.core import fetch_data, query_apis


celery = create_celery()
celery.autodiscover_tasks(['events.tasks'])
    