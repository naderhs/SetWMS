from django.apps import AppConfig


class SetAppConfig(AppConfig):
    name = 'set_app'

    def ready(self):
        import set_app.signals
