from django.apps import AppConfig


class SubjectsConfig(AppConfig):
    name = "apps.subjects"

    def ready(self):
        import apps.subjects.signals
