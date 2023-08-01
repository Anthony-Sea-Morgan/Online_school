import logging
from logging.handlers import RotatingFileHandler
from celery import Celery
from django.conf import settings
from datetime import timedelta
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


app = Celery('it_school')

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

CELERY_BEAT_SCHEDULE = {
    'send_reminder_email_task': {
        'task': 'it_school.tasks.send_reminder_email_task',
        'schedule': timedelta(minutes=1),
        'options': {
            'expires': 60,
        },
    },
}
CELERY_BEAT_MAX_INTERVAL = 60

# Создаем логгер с именем 'celery'
logger = logging.getLogger('celery')

# Устанавливаем уровень логирования (в данном случае INFO)
logger.setLevel(logging.INFO)

# Создаем обработчик RotatingFileHandler для записи логов в файл celery.log
log_file = 'celery.log'
handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)  # 10 MB
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(handler)

# Загружаем настройки из объекта Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

if __name__ == '__main__':
    app.start()

# Автоматически находим и регистрируем задачи (таски) из приложения it_school
app.autodiscover_tasks(['it_school'])

