import importlib

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'krit.teams'
    label = "krit_teams"

    def ready(self):
        importlib.import_module("krit.teams.receivers")