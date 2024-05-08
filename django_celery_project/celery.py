from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "django_celery_project.settings"
)
app = Celery("django_celery_project")
app.conf.enable_utc = False
app.config_from_object(settings, namespace="CELERY")
app.conf.beat_schedule = {}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# BEAT SCHDEULE
app.conf.beat_schedule = {
    "every-10-minutes": {
        "task": "mainapp.tasks.update_subscription_time",
        # for every ten minutes 60s*10m
        "schedule": 600,
    }
}
app.autodiscover_tasks()
