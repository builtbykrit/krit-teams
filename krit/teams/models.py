from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from .conf import settings


def load_model_class(model_path):
    dot = model_path.rindex('.')
    module_name = model_path[:dot]
    class_name = model_path[dot + 1:]
    try:
        _class = getattr(import_module(module_name), class_name)
        return _class
    except (ImportError, AttributeError):
        raise ImproperlyConfigured('%s cannot be imported' % model_path)

class Team(load_model_class(settings.KRIT_TEAMS_BASE_TEAM_MODEL)):
    class Meta(load_model_class(settings.KRIT_TEAMS_BASE_TEAM_MODEL).Meta):
        verbose_name = "Team"
        verbose_name_plural = "Teams"


class Membership(load_model_class(settings.KRIT_TEAMS_BASE_MEMBERSHIP_MODEL)):

    team = models.ForeignKey(Team,
                             related_name="memberships",
                             verbose_name="team",
                             on_delete=models.CASCADE)

    class Meta(load_model_class(settings.KRIT_TEAMS_BASE_MEMBERSHIP_MODEL).Meta):
        unique_together = [("team", "user", "invitation")]
        verbose_name = "Membership"
        verbose_name_plural = "Memberships"


