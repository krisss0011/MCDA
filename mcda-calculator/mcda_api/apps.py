from django.apps import AppConfig
from django.db.models.signals import post_migrate


class McdaApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mcda_api'

    def ready(self):
        from . import signals
        post_migrate.connect(signals.run_on_post_migrate, sender=self)
