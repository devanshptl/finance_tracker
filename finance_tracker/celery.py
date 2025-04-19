from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module for 'celery'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance_tracker.settings")

app = Celery("finance_tracker")

# Load settings from Django settings module
app.config_from_object("django.conf:settings", namespace="CELERY")

# Ensure Django is loaded before Celery tries to discover tasks
import django

django.setup()

# Discover tasks in all registered apps
app.autodiscover_tasks()
