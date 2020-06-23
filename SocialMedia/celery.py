from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SocialMedia.settings")
app1 = Celery("SocialMedia")

app1.config_from_object("django.conf:settings")


app1.autodiscover_tasks(settings.INSTALLED_APPS)