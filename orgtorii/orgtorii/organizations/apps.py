from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orgtorii.organizations"
    verbose_name = "Organizations"

    def ready(self):
        """Import rules when app is ready."""
        from . import rules  # noqa: F401
