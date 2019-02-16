from django.apps import AppConfig


class BooktimeConfig(AppConfig):
    name = 'booktime'

    def ready(self):
        """This is enough to make sure that signals are registered"""
        from . import signals
