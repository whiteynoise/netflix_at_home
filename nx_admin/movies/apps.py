from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MoviesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "movies"
    verbose_name = _("Movie")
    verbose_name_prular = _("Movies")

    def ready(self):
        import movies.signals