from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save


class FlagsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orgtorii.flags"
    verbose_name = "Feature Flags"

    def ready(self):
        """Set up cache invalidation signals when flags are saved or deleted."""
        from orgtorii.flags.models import FeatureFlag
        from orgtorii.flags.providers import DjangoFlagProvider

        provider = DjangoFlagProvider()

        def invalidate_flag_cache(sender, instance, **kwargs):
            """Invalidate cache when a flag is saved or deleted."""
            provider.invalidate_cache(instance.name)

        post_save.connect(invalidate_flag_cache, sender=FeatureFlag)
        post_delete.connect(invalidate_flag_cache, sender=FeatureFlag)

