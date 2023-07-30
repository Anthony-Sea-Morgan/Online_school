from celery import Celery
from django.conf import settings
from datetime import timedelta

app = Celery('it_school')

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

CELERY_BEAT_SCHEDULE = {
    'send_reminder_email_task': {
        'task': 'it_school.tasks.send_reminder_email_task',
        'schedule': timedelta(days=7),
        'options': {
            'expires': 60,
        },
    },
}
CELERY_BEAT_MAX_INTERVAL = 60

app.config_from_object('django.conf:settings', namespace='CELERY')

if __name__ == '__main__':
    app.start()


app.autodiscover_tasks(['it_school'])
