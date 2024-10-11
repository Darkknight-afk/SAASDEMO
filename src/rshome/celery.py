import os
from celery import Celery
from decouple import config
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rshome.settings')

app = Celery('rshome')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()