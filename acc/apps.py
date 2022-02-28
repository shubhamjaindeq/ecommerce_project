"""Configuration for this app"""
from django.apps import AppConfig


class AccConfig(AppConfig):
    """signal config"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'acc'

    def ready(self):
        import acc.signals
