import os
from celery import Celery
# название папки, где лежат settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eoscan_app.settings')
celery_app = Celery('recognition_c')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
# сама найдет отложенные задачи
celery_app.autodiscover_tasks()
# запуск celery -A eoscan_app worker -l info
