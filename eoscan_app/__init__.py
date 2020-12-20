from .celery import celery_app

# переменная будет видна во всех приложениях
__all__ = ('celery_app',)
