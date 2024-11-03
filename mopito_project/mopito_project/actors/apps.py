from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ActorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mopito_project.actors'
    verbose_name = _("Actors")
