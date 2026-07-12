from django.apps import AppConfig


class AppCoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.app_core"
    label = "app_core"

    def ready(self):
        import apps.app_core.signals 