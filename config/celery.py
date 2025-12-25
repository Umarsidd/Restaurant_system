"""
Celery configuration for Restaurant System
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('restaurant_system')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'auto-close-abandoned-tables': {
        'task': 'notifications.tasks.auto_close_abandoned_tables',
        'schedule': crontab(minute=0),  # Every hour
    },
    'alert-pending-bills': {
        'task': 'notifications.tasks.alert_pending_bills',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
