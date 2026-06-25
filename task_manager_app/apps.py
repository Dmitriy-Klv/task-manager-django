from django.apps import AppConfig


class TestAppConfig(AppConfig):
    name = "task_manager_app"

    def ready(self):
        import task_manager_app.signals
