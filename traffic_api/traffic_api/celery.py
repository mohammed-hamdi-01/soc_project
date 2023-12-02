import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_api.settings')

app = Celery('traffic_api')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all apps
app.autodiscover_tasks()
