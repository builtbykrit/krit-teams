import importlib

# Import settings from django.conf before
# importing appconf.AppConf
# https://pypi.python.org/pypi/django-appconf
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from appconf import AppConf


def load_path_attr(path):
    i = path.rfind(".")
    module, attr = path[:i], path[i + 1:]
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured("Error importing {0}: '{1}'".format(module, e))
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured("Module '{0}' does not define a '{1}'".format(module, attr))
    return attr


class TeamAppConf(AppConf):

    HOOKSET = "krit.teams.hooks.TeamDefaultHookset"
    BASE_TEAM_MODEL = "krit.teams.base_models.BaseTeam"
    BASE_MEMBERSHIP_MODEL = "krit.teams.base_models.BaseMembership"
    ROLE_MEMBER = "member"
    ROLE_OWNER = "owner"
    ROLE_CHOICES = [
        (ROLE_MEMBER, "member"),
        (ROLE_OWNER, "owner")
    ]

    class Meta:
        prefix = "krit_teams"

    def configure_hookset(self, value):
        return load_path_attr(value)()