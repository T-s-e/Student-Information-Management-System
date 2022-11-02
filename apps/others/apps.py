from django.apps import AppConfig


class OthersConfig(AppConfig):
    name = "apps.others"

    def ready(self):
        import apps.others.signals
